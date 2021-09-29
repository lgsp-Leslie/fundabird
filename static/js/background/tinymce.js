$(() => {
    //设置富文本编辑器
    tinymce.init({
        selector: '.textarea',
        // language: 'zh_CN',
        plugins: 'print preview searchreplace autolink directionality visualblocks visualchars fullscreen image link media template code codesample table charmap hr pagebreak nonbreaking anchor insertdatetime advlist lists wordcount imagetools textpattern help emoticons autosave bdmap indent2em autoresize formatpainter axupimgs',
        toolbar: 'code undo redo restoredraft | cut copy paste pastetext | forecolor backcolor bold italic underline strikethrough link anchor | alignleft aligncenter alignright alignjustify outdent indent | \
    styleselect formatselect fontselect fontsizeselect | bullist numlist | blockquote subscript superscript removeformat | \
    table image media charmap emoticons hr pagebreak insertdatetime print preview | fullscreen | bdmap indent2em lineheight formatpainter axupimgs',
        max_height: 600,
        min_height: 600,
        height: 600,
        inline: false,
        menubar: true,
        quickbars_selection_toolbar: 'bold italic | link h2 h3 blockquote',
        quickbars_insert_toolbar: 'quickimage quicktable',
        images_upload_url: '/manage/tiny_upload',
        images_upload_base_path:'/static',
    })
})