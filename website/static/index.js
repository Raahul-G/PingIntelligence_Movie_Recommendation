function deleteNote(noteId) {
  fetch("/delete-note", {                       // send a request to an endpoint called delete-note
    method: "POST",                             // sending a post request
    body: JSON.stringify({ noteId: noteId }),   // sending the note id
  }).then((_res) => {                           // after getting a response from delete-note window
    window.location.href = "/";                 // it will reload the home page (note page in this case)
  });
}