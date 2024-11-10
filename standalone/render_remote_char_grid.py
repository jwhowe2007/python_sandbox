import pandas as pd

url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"

def dump_google_doc_chars(url):
    dataframes = pd.read_html(url, header=0, encoding='utf-8')

    for dataframe in dataframes:
        grid_cells = {}
        df = pd.melt(dataframe, id_vars=['x-coordinate', 'y-coordinate'])

        # Convert the dataframe to a grid of points containing unicode characters
        for row_index, row_data in df.iterrows():
            x_coord, y_coord = row_data['x-coordinate'], row_data['y-coordinate']
            character = row_data['value']

            # Build the cells array
            grid_cells[(x_coord, y_coord)] = character

        # determine size of grid
        max_x = max(point[0] for point in grid_cells)
        max_y = max(point[1] for point in grid_cells)

        # Build out the grid shape, leaving room for one extra space in either direction
        grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

        # Set the given character at each given point coordinate
        for (x, y), char in grid_cells.items():
            grid[y][x] = char

        # Print the grid by rendering each row joined into a string
        for y in range(max_y, -1, -1):
            print(''.join(grid[y]))

dump_google_doc_chars(url)

