def create_staircase(nums):
    step = 1
    subsets = []

    while nums != []:
        print(f"Nums: {nums}\tStep: {step}\tSubsets: {subsets}")
        if len(nums) >= step:
            subsets.append(nums[0:step])
            nums = nums[step:]
            step += 1
        else:
            return False

    return subsets

numbers = [1, 2, 3, 4, 5, 6, 7]
print(f"Create staircase out of {numbers}: {create_staircase(numbers)}")


