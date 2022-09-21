import boto3


def add_photo_url_to_context(request):
    try:
        client = boto3.client(
            's3',
            aws_access_key_id='AKIAIIQH747JZ5ZFDPIA',
            aws_secret_access_key='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',
        )
        client.get_object(Bucket='3240-Profile-Pictures'.lower(), Key=request.user.username + '.jpg')
        pic_url = 'https://s3.amazonaws.com/3240-profile-pictures/' + request.user.username + '.jpg'
    except Exception as ex:
        pic_url = None
    return {
        'picture_url': pic_url,
    }