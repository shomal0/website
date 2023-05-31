function deleteNote(noteId, groupIndex) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ note_id: noteId, group_index: groupIndex }),
  }).then((_res) => {
    window.location.href = "/group?group_index=" + groupIndex;
  });
}
