'use strict';

$(async function () {
  $("#unlike").on("click", unlike);
  $("#like").on("click", like);

  let response = await axios.get("/api/likes", {params: { cafe_id: cafeId }});
  let result = response.data;
  console.log(response.data);

  if ("error" in result) {
    console.log(result.error);
  } else {
    let likes = result.likes;
    if (likes) $("#unlike").show();
    else $("#like").show();
  }
});

async function unlike(evt) {
  evt.preventDefault();

  let response = await axios.post("/api/unlike", { cafe_id: cafeId });
  let result = response.data;

  if ("error" in result) {
    console.log(result.error);
  } else {
    $("#unlike").hide();
    $("#like").show();
  }
}

async function like(evt) {
  evt.preventDefault();

  let response = await axios.post("/api/like", { cafe_id: cafeId });
  let result = response.data;

  if ("error" in result) {
    console.log(result.error);
  } else {
    $("#like").hide();
    $("#unlike").show();
  }
}