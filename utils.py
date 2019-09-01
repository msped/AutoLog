def votes(user_email, build_votes):
    if user_email in build_votes:
        return True
    return False


def new_build_content(exterior, engine, running, interior, request, users,
                      build_author):
    record = {
        'author': build_author,
        'build_name': request.form.get('build_name'),
        'total': float(request.form.get('total')),
        'visibility': request.form.get('visibility'),
        'car': {
            'make': request.form.get('make'),
            'model': request.form.get('model'),
            'trim': request.form.get('trim'),
            'year': request.form.get('year'),
            'price': float(request.form.get('price'))
        },
        'votes': {
            'like': {
                'count': 1,
                'users_liked': users
            },
            'dislike': {
                'count': 0,
                'users_disliked': []
            }
        },
    }

    # Adds exterior collection to record
    exterior_dict = {}
    for item in exterior:
        product = request.form.get('exterior_'+item["part_id"]+'_product')
        if product is not None:
            exterior_dict.update({
                item["part_id"]: {
                    'product': product,
                    'link': request.form.get(
                        'exterior_'+item["part_id"]+'_link'
                    ),
                    'price': float(request.form.get(
                        'exterior_'+item["part_id"]+'_price'
                    ))
                }
            })
    record.update({'exterior': exterior_dict})

    # Adds Engine collection to record
    engine_dict = {}
    for item in engine:
        product = request.form.get('engine_'+item["part_id"]+'_product')
        if product is not None:
            engine_dict.update({
                item["part_id"]: {
                    'product': product,
                    'link': request.form.get(
                        'engine_'+item["part_id"]+'_link'
                    ),
                    'price': float(request.form.get(
                        'engine_'+item["part_id"]+'_price'
                    ))
                }
            })

    record.update({'engine': engine_dict})

    # Adds Running Gear collection to record
    running_dict = {}
    for item in running:
        product = request.form.get('running_'+item["part_id"]+'_product')
        if product is not None:
            running_dict.update({
                item["part_id"]: {
                    'product': product,
                    'link': request.form.get(
                        'running_'+item["part_id"]+'_link'
                    ),
                    'price': float(request.form.get(
                        'running_'+item["part_id"]+'_price'
                    ))
                }
            })

    record.update({'running': running_dict})

    # Adds Interior collection to record
    interior_dict = {}
    for item in interior:
        product = request.form.get('interior_'+item["part_id"]+'_product')
        if product is not None:
            interior_dict.update({
                item["part_id"]: {
                    'product': product,
                    'link': request.form.get(
                        'interior_'+item["part_id"]+'_link'
                    ),
                    'price': float(request.form.get(
                        'interior_'+item["part_id"]+'_price'
                    ))
                }
            })

    record.update({'interior': interior_dict})

    return record


def update_build_content(exterior, engine, running, interior, request):

    record = {
        'total': float(request.form.get('total')),
        'visibility': request.form.get('visibility'),
        'car': {
            'make': request.form.get('make'),
            'model': request.form.get('model'),
            'trim': request.form.get('trim'),
            'year': request.form.get('year'),
            'price': float(request.form.get('price'))
        },
    }

    # Adds exterior collection to record
    exterior_dict = {}
    for item in exterior:
        product = request.form.get('exterior_'+item["part_id"]+'_product')
        if product is not None:
            exterior_dict.update({
                item["part_id"]: {
                    'product': product,
                    'link': request.form.get(
                        'exterior_'+item["part_id"]+'_link'
                    ),
                    'price': float(request.form.get(
                        'exterior_'+item["part_id"]+'_price'
                    ))
                }
            })

    record.update({'exterior': exterior_dict})

    # Adds Engine collection to record
    engine_dict = {}
    for item in engine:
        product = request.form.get('engine_'+item["part_id"]+'_product')
        if product is not None:
            engine_dict.update({
                item["part_id"]: {
                    'product': product,
                    'link': request.form.get(
                        'engine_'+item["part_id"]+'_link'
                        ),
                    'price': float(request.form.get(
                        'engine_'+item["part_id"]+'_price'
                    ))
                }
            })

    record.update({'engine': engine_dict})

    # Adds Running Gear collection to record
    running_dict = {}
    for item in running:
        product = request.form.get('running_'+item["part_id"]+'_product')
        if product is not None:
            running_dict.update({
                item["part_id"]: {
                    'product': product,
                    'link': request.form.get(
                        'running_'+item["part_id"]+'_link'
                    ),
                    'price': float(request.form.get(
                        'running_'+item["part_id"]+'_price'
                    ))
                }
            })

    record.update({'running': running_dict})

    # Adds Interior collection to record
    interior_dict = {}
    for item in interior:
        product = request.form.get('interior_'+item["part_id"]+'_product')
        if product is not None:
            interior_dict.update({
                item["part_id"]: {
                    'product': product,
                    'link': request.form.get(
                        'interior_'+item["part_id"]+'_link'
                    ),
                    'price': float(request.form.get(
                        'interior_'+item["part_id"]+'_price'
                    ))
                }
            })

    record.update({'interior': interior_dict})

    return record
