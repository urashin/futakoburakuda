"use strict";


// Queries
// 間違ってるかもしれないのでまとめておく
const POST_QUERY = '.userContentWrapper';
const MESSAGE_QUERY = '[data-testid="post_message"]'; //'.userContent';
const IMAGE_QUERY = 'img.scaledImageFitWidth, img.scaledImageFitHeight';
const FETCHE_TARGET_QUERY = '[role="feed"]';//'#u_fetchstream_1_0 > div';
const FETCHED_POST_QUERY = '._5jmm';


// 後読みされるPostを取得する
function getFetchedPosts(callback) {
  const target = document.querySelector(FETCHE_TARGET_QUERY).childNodes[2];
  const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
      if(mutation.addedNodes.length) {
        const posts = [].slice.call(mutation.addedNodes)
          .map(e => getPosts(e, FETCHED_POST_QUERY))
          .filter(x => x.length)[0];
        posts && callback(posts);
      }
    })
  });
  observer.observe(target, {childList: true, subtree: true});
}

// 投稿全体を取得
function getPosts(_target, _query) {
  const target = _target || document.getElementById('contentArea');
  const query = _query || POST_QUERY;
  const posts = target.nodeType === 1 ? target.querySelectorAll(query) : [];
  return [].slice.call(posts);
}

// 投稿からテキストを取得
function getMessageFromPost(post) {
  const texts = post.querySelectorAll(MESSAGE_QUERY);
  const items = [].slice.call(texts).filter(x => !!x);
  const data =  items.reduce((acc, texts) => {
    return acc + texts.textContent
  }, '');
  return {
    items,
    data,
  }
}

// 投稿から画像を取得
function getImagesFromPost(post) {
  const images = post.querySelectorAll(IMAGE_QUERY);
  const items = [].slice.call(images).filter(x => !!x);
  const data =  items.map(e => ({
    url: e.src,
    alt: e.alt
  }));
  return {
    items,
    data,
  }
}

// 投稿から画像/テキストどちらも取得して整形して返す
function getBoth(post) {
  const text = getMessageFromPost(post);
  const image = getImagesFromPost(post);
  return {
    text,
    image,
  };
}

// sleep util function
// Mutate検知後すぐだと要素が取れないので
function sleep(msec) {
  return new Promise(function(resolve) {
    setTimeout(function() {resolve()}, msec);
  })
}

// backgroundに画像POST依頼を投げて返ってきたパスで画像を書き換える
function changeImage(posts) {
  posts.forEach(item => {
    const insert = (res) => {
      const changed = res.imgPath;
      // TODO: まだパスが返ってこないのでalt変えてみる。ちゃんと結合したらsrcを変える
      item.image.items.map(x => x.alt = changed);
    };
    item.image.data.forEach(data => {
      chrome.runtime.sendMessage(
        { task: 'postImage',
          data: data,
        },
        insert
      );
    })
  });
}

// backgroundにテキストPOST依頼を投げて返ってきた文字列でメッセージを入れ替える
function changeText(posts) {
  posts.forEach(item => {
    const insert = (res) => {
      if(res) {
        const changed = 'modified: ' + res.text;
        item.text.items.map(x => x.innerText = changed);
      }
    };
    chrome.runtime.sendMessage(
      { task: 'postText',
        data: {
          text: item.text.data,
        },
      },
      insert
    );
  });
}

(function () {
  const posts = getPosts();
  const first = posts.map(getBoth);
  console.log('初回分');
  console.log(first);

  changeText(first);
  changeImage(first);

  getFetchedPosts(async function(list) {
    await sleep(600);
    const added = list.map(post => getBoth(post));
    console.log('追加読み込み分');
    console.log(added);
    changeText(added);
    changeImage(added);
  })

})();


