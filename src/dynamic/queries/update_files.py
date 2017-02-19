def update_files_with_query(filename):
    return {
        "script":
            "def updated = false; def file=['filename':'" + filename + "', 'error_count':1]; for (int i=0;i<ctx._source.files.size();i++) { if (ctx._source.files[i]['filename'] == file['filename']){ctx._source.files[i].error_count += 1; updated=true;break}}if(!updated){ctx._source.files.add(file)}"
    }