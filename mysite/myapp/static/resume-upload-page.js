var dropZone = document.getElementById('drop-zone');
  var fileUpload = document.getElementById('file-upload');
  var fileBrowse = document.getElementById('file-browse');
  var preview = document.querySelector('.upload-preview');

  fileUpload.addEventListener('change', function(e) {
    var files = e.target.files;
    handleFiles(files);
  });

  dropZone.addEventListener('dragover', function(e) {
    e.stopPropagation();
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
    dropZone.classList.add('drop');
  });

  dropZone.addEventListener('dragleave', function(e) {
    e.stopPropagation();
	e.preventDefault();
    dropZone.classList.remove('drop');
  });

  dropZone.addEventListener('drop', function(e) {
    e.stopPropagation();
    e.preventDefault();
    var files = e.dataTransfer.files;
    handleFiles(files);
    dropZone.classList.remove('drop');
  });

  fileBrowse.addEventListener('click', function(e) {
    e.stopPropagation();
    e.preventDefault();
    fileUpload.click();
  });

  function handleFiles(files) {
    for (var i = 0; i < files.length; i++) {
      var file = files[i];
      var option = document.createElement('option');
      option.value = file.name;
      option.text = file.name;
      fileUpload.appendChild(option);

      if (file.type === 'application/pdf') {
        var div = document.createElement('div');
        div.classList.add('pdf-file');


        var deleteButton = document.createElement('span');
        deleteButton.classList.add('delete-file');
        deleteButton.textContent = 'Delete Current File';
        deleteButton.addEventListener('click', function(e) {
          div.parentNode.removeChild(div);
          option.parentNode.removeChild(option);
          fileUpload.value = '';
        });
        div.appendChild(deleteButton);

        var fileName = document.createElement('p');
        fileName.classList.add('file-name');
        fileName.textContent = file.name;
        div.appendChild(fileName);

        var object =document.createElement('object');
        object.classList.add('pdf-preview');
        object.setAttribute('type', 'application/pdf');
        object.setAttribute('data', URL.createObjectURL(file) + '#page=1&zoom=80');
        object.setAttribute('title', file.name);

        div.appendChild(object);
        preview.appendChild(div);
      }
    }
}