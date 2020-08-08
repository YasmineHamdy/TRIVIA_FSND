
def paginate(request, collection, pageSize):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * pageSize
  end = start + pageSize

  formatedCollection = [item.format() for item in collection]
  selection = formatedCollection[start:end]

  return selection
