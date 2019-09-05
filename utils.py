def votes(user_email, build_votes):
    if user_email in build_votes:
        return True
    return False


def get_heading_contents(request, heading, heading_name):
    heading_content = {}
    for item in heading:
        product = request.form.get(heading_name + item["part_id"] + '_product')
        if product is not None:
            heading_content.update({
                item["part_id"]: {
                    'product': product,
                    'link': request.form.get(
                        heading_name + item["part_id"] + '_link'
                    ),
                    'price': float(request.form.get(
                        heading_name + item["part_id"] + '_price'
                    ))
                }
            })
    return heading_content


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
    record.update({'exterior': get_heading_contents(request, exterior,
                                                    'exterior_')})

    # Adds Engine collection to record
    record.update({'engine': get_heading_contents(request, engine, 'engine_')})

    # Adds Running Gear collection to record
    record.update({'running': get_heading_contents(request, running,
                                                   'running_')})

    # Adds Interior collection to record
    record.update({'interior': get_heading_contents(request, interior,
                                                    'interior_')})

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
    record.update({'exterior': get_heading_contents(request, exterior,
                                                    'exterior_')})

    # Adds Engine collection to record
    record.update({'engine': get_heading_contents(request, engine,
                                                  'engine_')})

    # Adds Running Gear collection to record
    record.update({'running': get_heading_contents(request, running,
                                                   'running_')})

    # Adds Interior collection to record
    record.update({'interior': get_heading_contents(request, interior,
                                                    'interior_')})

    return record
