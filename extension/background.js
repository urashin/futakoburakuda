function fetchData(url = ``, data = {}) {
  // 既定のオプションには * が付いています
  return fetch(url, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, cors, *same-origin
    cache: "default", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "omit", // include, same-origin, *omit
    headers: {
      "Content-Type": "application/json",
    },
    redirect: "follow", // manual, *follow, error
    referrer: "no-referrer", // no-referrer, *client
    body: JSON.stringify(data), // 本文のデータ型は "Content-Type" ヘッダーと一致する必要があります
  })
    .then(res => res.json()) // レスポンスの JSON を解析
}


function postText(text) {
  const API = 'http://127.0.0.1:8080/transform';
  if(text) {
    return fetchData(API, {text: text})
  }
}

function postImage(data) {
  const API = 'http://127.0.0.1:8081/transform';
  return fetchData(API, data);
}

chrome.runtime.onMessage.addListener(
  function (request, sender, sendResponse) {
    var task = request.task;
    var data = request.data;

    switch (task) {
      // テキストの変換をする
      case "postText":
        if(data.text) {
          postText(data.text).then(res => sendResponse(res));
        }
        return true;

      // 画像の変換をする
      case 'postImage':
        if(data && data.url && data.alt) {
          postImage(data).then(res => sendResponse(res));
        }
        return true;
      default :
        return;
    }
  }
);