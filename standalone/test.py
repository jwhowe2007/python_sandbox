import arcpy as ap
import os

class FeatureDict(dict):
    """
    Extended Dictionary representation of ArcGIS Feature Classes and Layers. The class object is a dictionary with keys
    representing the ObjectIDs of collected features, and their corresponding values are another sub-dictionary. These
    sub-dictionaries are individual rows in the initialization layer; their keys are strings representing the names of
    fields of collected features, and their corresponding values are the table values of those fields for that record.
    """
    def __init__(self, f_class, fill=True):
        """
        Initializes the object using details and data found in the input layer object or feature class.

        :param f_class: ArcPy Layer object or a string representing a complete file path to feature class
        :param fill: boolean to determine if the FeatureDict should be filled upon instantiation
        """
        super(FeatureDict, self).__init__(self)
        self.disallowed = ['SHAPE.STLENGTH()', 'SHAPE.STAREA()']
        self.fields = [f.name.upper() for f in ap.ListFields(f_class) if f.name.upper() not in self.disallowed]
        self.tokens = None
        self.layer = f_class
        self.name = os.path.split(self.layer.__str__())[-1]
        self.spatial_ref = ap.Describe(self.layer).spatialReference
        self.geom_type = ap.Describe(self.layer).shapeType
        try:
            self.last = [s_row[0] for s_row in ap.da.SearchCursor(self.layer, 'OID@')][-1]
        except IndexError:
            self.last = 1
        try:
            self.selected = [int(fid) for fid in ap.Describe(self.layer).FIDSet.split(';')]
        except (ValueError, AttributeError):
            self.selected = []
        self.tokenize()
        if fill:
            self.fill(self.selected)

    def __str__(self):
        """
        String representation of the object.

        :return: string
        """
        return 'Dictionary representation of feature class: {}'.format(self.layer)

    def __repr__(self):
        """
        String representation of reproducing the object.

        :return: string
        """
        return 'FeatureDict({})'.format(self.layer)

    def tokenize(self):
        """
        Sets token property of the object to be an ArcPy cursor compliant list of strings.

        :return: None
        """
        self.tokens = list(self.fields)
        for bad_token in ['OBJECTID', 'SHAPE']:
            if bad_token in self.tokens:
                self.tokens.remove(bad_token)
        self.tokens.append('SHAPE@')
        self.tokens.append('OID@')

    def feature_count(self):
        """
        Determines the number of features collected in the FeatureDict.

        :return: integer, number of features stored in the FeatureDict
        """
        return len(self.keys())

    def is_empty(self):
        """
        Determines if the FeatureDict is empty or contains key, value pairs.

        :return: boolean, True means the FeatureDict is empty
        """
        if self.feature_count() == 0:
            return True
        return False

    def insert(self, row_dict):
        """
        Insert the passed dictionary into the FeatureDict. The dictionary must contain keys which match values in the
        FeatureDict's fields. If an OID field is passed (as a key in row_dict), it will be overridden with the next
        available ObjectID.

        :param row_dict: dictionary
        :return: boolean, True if row was inserted successfully
        """
        if not isinstance(row_dict, dict):
            return False
        for row_key in row_dict.keys():
            if row_key not in self.fields:
                del row_dict[row_key]
        for dict_field in self.fields:
            if dict_field not in row_dict.keys():
                row_dict[dict_field] = None
        row_dict['OID'] = self.last + 1
        row_dict['OBJECTID'] = self.last + 1
        self[self.last + 1] = row_dict
        self.last += 1
        return True

    def fill(self, select_list=()):
        """
        Populates the object with dictionaries whose key, value pairs represent field names and values from the
        initialization layer or feature class, respectively. These dictionaries can be accessed via the object itself,
        whose keys are ObjectID values found in the initialization layer or feature class. ObjectIDs passed into the
        method in the select_list list will be the only ObjectIDs collected.

        :param select_list: list or tuple of integers representing selected ObjectIDs
        :return: None
        """
        self.clear()
        with ap.da.SearchCursor(self.layer, self.tokens) as fc_cursor:
            for feature_row in fc_cursor:
                feature_oid = feature_row[-1]
                if len(select_list) > 0:
                    if feature_oid not in select_list:
                        continue
                self[feature_oid] = {}
                for field_name in self.tokens:
                    field_index = self.tokens.index(field_name)
                    field_name = field_name if '@' not in field_name else field_name.split('@')[0]
                    self[feature_oid][field_name] = feature_row[field_index]

    def project(self, proj_wkid):
        """
        Reprojects all geometry data in the object to the provided spatial reference Well Known ID (WKID)

        :param proj_wkid: int, WKID of output spatial reference
        :return: boolean, True if operation is success, False otherwise
        """
        if not isinstance(proj_wkid, int):
            return False
        try:
            self.spatial_ref = ap.SpatialReference(proj_wkid)
        except RuntimeError:
            return False
        for item in self.keys():
            item_shp = self[item]['SHAPE']
            proj_shp = item_shp.projectAs(self.spatial_ref)
            self[item]['SHAPE'] = proj_shp
        return True

    def update_layer(self, target_layer=None, target_fields=None, add_new=False):
        """
        Updates the target_layer (initialization layer by default) using the data in this object. This is done via
        matching ObjectID values, so it is recommended to not set the target_layer keyword argument unless you must.

        :param target_layer: ArcPy Layer object or a string representing the complete path to an existing feature class
        :param target_fields: list of strings representing fields shared by the initialization layer and the target
                              layer which will be updated
        :param add_new: boolean, if True the update_layer operation will add new features whose key value in the
                        FeatureDict are not represented in the initialization layer
        :return: boolean, success or failure of operation
        """
        if target_layer is None:
            target_layer = self.layer
        if not ap.Exists(target_layer):
            print('Parameter Error: {} does not exist.'.format(target_layer))
            return False
        if target_fields is None:
            target_fields = self.tokens
        if 'OID@' not in target_fields:
            target_fields.append('OID@')
        try:
            if add_new:
                existing_oids = []
                with ap.da.SearchCursor(target_layer, 'OID@') as cursor:
                    for row in cursor:
                        existing_oids.append(row[0])
                insert_fields = target_fields
                if 'OBJECTID' in insert_fields:
                    insert_fields.remove('OBJECTID')
                s_cursor = ap.da.InsertCursor(target_layer, insert_fields)
                for row_oid in self.keys():
                    if row_oid not in existing_oids:
                        new_row = [None for _ in insert_fields]
                        for s_field in insert_fields:
                            if s_field == 'OID@':
                                s_index = insert_fields.index('OID@')
                                new_row[s_index] = row_oid
                            else:
                                s_index = insert_fields.index(s_field)
                                new_row[s_index] = self[row_oid][insert_fields[s_index].split('@')[0]]
                        s_cursor.insertRow(new_row)
            with ap.da.UpdateCursor(target_layer, target_fields) as s_cursor:
                for s_row in s_cursor:
                    row_oid = s_row[target_fields.index('OID@')]
                    if row_oid in self.keys():
                        for s_field in target_fields:
                            if s_field == 'OID@':
                                continue
                            s_index = target_fields.index(s_field)
                            s_row[s_index] = self[row_oid][target_fields[s_index].split('@')[0]]
                        s_cursor.updateRow(s_row)
        except RuntimeError:
            return False
        return True

    def export(self, target_dest):
        """
        Exports the data in the object to the passed File GeoDatabase with the same name as the initialization layer or
        feature class. This operation can create duplicate data if the targeted feature class/dataset already exists.
        The target GeoDatabase does not need to exist, but it's parent directory must exist at run time. If the data is
        to be exported into a Feature Dataset, it does not need to exist beforehand.

        :param target_dest: string representing a complete path to a GeoDatabase or a Feature Class
        :return: boolean, success or failure of operation
        """
        if '.GDB' not in target_dest.upper():
            print("Parameter Error: {} must at least be a path to a GeoDatabase".format(target_dest))
            return False
        if target_dest.upper().endswith('.GDB'):
            gdb_path = target_dest
            gdb_name = os.path.split(gdb_path)[-1]
            target_dest = os.path.dirname(target_dest)
            if not os.path.exists(target_dest):
                try:
                    os.mkdir(target_dest)
                except OSError as err:
                    print("OS Error: ", err)
                    return False
            if not ap.Exists(gdb_path):
                ap.management.CreateFileGDB(target_dest, gdb_name)
            fc_path = os.path.join(gdb_path, self.name)
            target_name = self.name
        else:
            depth_cnt = 0
            split_dest = target_dest.split(os.sep)
            target_name = split_dest[-1]
            for q in split_dest:
                if q.upper().endswith('.GDB'):
                    break
                depth_cnt += 1
            if len(split_dest) > depth_cnt + 2:
                gdb_path = os.sep.join(split_dest[:-2])
                if not gdb_path.upper().endswith('.GDB'):
                    print("Path Error: {} is too many children away from the GeoDatabase".format(target_dest))
                    return False
                if not ap.Exists(gdb_path):
                    ap.management.CreateFileGDB(os.path.dirname(gdb_path), os.path.split(gdb_path)[-1])
                target_dataset = split_dest[-2]
                ds_path = os.path.join(gdb_path, target_dataset)
                if not ap.Exists(ds_path):
                    ap.management.CreateFeatureDataset(gdb_path, target_dataset, spatial_reference=self.spatial_ref)
                fc_path = os.path.join(os.path.join(gdb_path, target_dataset), target_name)
            else:
                print('DEBUG: {}'.format(target_dest))
                fc_path = target_dest
                gdb_path = os.path.dirname(fc_path)
                while not target_dest.upper().endswith('.GDB'):
                    target_dest = os.path.dirname(target_dest)
                target_dest = os.path.dirname(target_dest)
                print('DEBUG {}'.format(target_dest))
                if not ap.Exists(target_dest):
                    ap.management.CreateFileGDB(target_dest, os.path.split(gdb_path)[-1])
        if not ap.Exists(fc_path):
            print('DEBUG: {}'.format(os.path.dirname(fc_path)))
            print('DEBUG: {}'.format(target_name))
            ap.CreateFeatureclass_management(os.path.dirname(fc_path), target_name, spatial_reference=self.spatial_ref,
                                             geometry_type=self.geom_type, template=self.layer)
        s_cursor = ap.da.InsertCursor(fc_path, self.tokens)
        s_oids = self.keys()
        s_oids.sort()
        for s_oid in s_oids:
            s_row = [None for _ in self.tokens]
            for s_field in self.tokens:
                s_index = self.tokens.index(s_field)
                s_row[s_index] = self[s_oid][s_field.split('@')[0]]
            s_cursor.insertRow(s_row)
        del s_cursor
        return True