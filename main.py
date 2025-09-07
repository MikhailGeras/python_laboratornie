def ts(nums,target):
  for el in nums:
    if not(isinstance(el, int)):
      return 'Не является целым числом'
    for i in range(len(nums)):
      for j in range(i+1, len(nums)):
        if nums[i] + nums[j] == target:
          return([i, j])
  return None