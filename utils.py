# Unzip .gz and return io.StringIO object
def unzip_xgz(file_name='', *args, **kwargs):
    with gzip.open(file_name, 'rb') as f_in:
        with open(get_uncompressed_file_name(file_name), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    return get_uncompressed_file_name(file_name)


def unzip_gz(*args, **kwargs):
    gfile = gzip.GzipFile(*args, **kwargs)
    zipped_buffer = StringIO()

    # Read gzipped file by chuncks until it finished with exception...
    try:
        while True:
            zipped_buffer.write(gfile.read1().decode('utf-8'))
    except OSError:
        pass

    zipped_buffer.seek(0)

    return zipped_buffer


def send_completed_email(dashboard_uri, user, file):
    msg_body = render_to_string('fileapi/file_success_msg.html', {
        'user': user.username,
        'filename': file.file_name,
        'dashboard': dashboard_uri
    })
    send_mail("Your analysis is ready", msg_body, settings.EMAIL_FROM, [user.email], html_message=msg_body)


def get_uncompressed_file_name(file_name):
    return "%s.uncompressed" % file_name


def get_s3_data_to_file(file_name):
    static_dir = 'staticfiles/'
    os.environ['S3_USE_SIGV4'] = S3_USE_SIGV4
    os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
    os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
    s3_client = boto3.client('s3')
    s3_client.download_file(settings.AWS_STORAGE_BUCKET_NAME, str(file_name), static_dir + file_name)
    return static_dir + file_name


# Unzip zipped file and return archive, unzipped file and name of unzipped file
def unzip_zip(file_name=''):
    archive = zipfile.ZipFile(file_name, 'r')
    name = archive.namelist()[0]
    file = archive.open(name)
    with open(get_uncompressed_file_name(file_name), 'wb') as f_out:
        f_out.write(file.read())
        f_out.close()
    return archive, get_uncompressed_file_name(file_name), name


def unzip_any_file(archive_file_name):
    mime_type = magic.from_file(archive_file_name, mime=True)
    print("Mime type: %s" % mime_type)
    if mime_type == 'application/gzip':
        file = unzip_xgz(file_name=archive_file_name)
        archive = None
        file_name = None
    elif mime_type == 'application/x-gzip':
        file = unzip_xgz(file_name=archive_file_name)
        archive = None
        file_name = None
    elif mime_type == 'application/zip':
        archive, file, file_name = unzip_zip(archive_file_name)
    elif mime_type == 'text/plain':
        file = archive_file_name
        archive = None
        file_name = None
    else:
        raise Exception("Cannot unzip file with mime type: %s" % mime_type)
    return archive, file, file_name


def handle_errors(file):
    e_t, e_o, tb = sys.exc_info()
    f = tb.tb_frame
    line = linecache.getline(f.f_code.co_filename, tb.tb_lineno, f.f_globals)
    file.status = File.FILE_STATUS_ERROR
    file.status_message = "Error line: %s (%s: %s): '%s'" % (tb.tb_lineno, e_t, e_o, line.strip(),)
    file.save()
    traceback.print_exc()
    print(file.status_message)


def s3_file_dwnld_url_utility(key_name, out_path):
    os.environ['S3_USE_SIGV4'] = S3_USE_SIGV4
    os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
    os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
    s3 = boto3.client('s3')

    try:
        if boto3.resource('s3').Object(settings.AWS_STORAGE_BUCKET_NAME, key_name).load():
            s3.delete_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=key_name
            )
    except:
        pass

    s3.upload_file(out_path, settings.AWS_STORAGE_BUCKET_NAME, key_name)
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': key_name
        }
    )

    return url

def work(func, *args):
    """Work function allows Multiprocessing to target functions that are otherwise out of scope"""
    for arg in args:
        func(arg)

def split(a, n):
    """Creates a generator object, splitting list(a) into n elements"""
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))
