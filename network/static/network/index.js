function like(post_id, user_id) {
  var btn_like = document.querySelector(`#btn_like_${post_id}`);
  fetch(`/like/${post_id}`, {
    method: "PUT",
    body: JSON.stringify({
      user_id: user_id,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      btn_like.innerHTML = `🤍${result.likes}`;
      btn_like.classList.remove("btn-danger");
      btn_like.classList.remove("btn-secondary");
      if (result.message === "liked") {
        btn_like.classList.add("btn-danger");
      } else {
        btn_like.classList.add("btn-secondary");
      }
      console.log(result.message);
      console.log(result.likes);
    });

  console.log(post_id, user_id);
}

function edit(post_id) {
  var content = document.querySelector(`#content_${post_id}`);
  var btn_edit = document.querySelector(`#btn_edit_${post_id}`);
  btn = btn_edit.innerHTML.toString().trim();

  if (btn === "Edit") {
    var text = content.innerText;
    console.log(text);
    content.innerHTML = `<textarea class='form-control' id='edit_text'></textarea>`;
    document.querySelector("#edit_text").innerHTML = text;
    btn_edit.innerHTML = "Save";
  } else {
    console.log("save");
    var new_text = document.querySelector("#edit_text");
    console.log(new_text.value);

    fetch(`/edit/${post_id}`, {
      method: "PUT",
      body: JSON.stringify({
        content: new_text.value,
      }),
    })
      .then((response) => response.json())
      .then((result) => {
        // update content and button
        content.innerHTML = result.content;
        btn_edit.innerHTML = "Edit";

        console.log(result);
      });
  }
}
