"use strict";

const POST_QUERY = '.userContentWrapper';
const MESSAGE_QUERY = '[data-testid="post_message"]'; //'.userContent';
const IMAGE_QUERY = 'img.scaledImageFitWidth'

function getFetchedPosts(callback) {
  const TERGET_QUERY = '#u_fetchstream_1_0 > div';
  const POST_QUERY = '._5jmm';

  const target = document.querySelector('[role="feed"]').childNodes[2];
  const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
      // console.log('mutation', mutation.addedNodes);
      // do something
      if(mutation.addedNodes.length) {
        const posts = [].slice.call(mutation.addedNodes)
          .map(e => getPosts(e, POST_QUERY))
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
  const messages = post.querySelectorAll(MESSAGE_QUERY);
  return [].slice.call(messages).reduce((acc, message) => {
    return acc + message.textContent
  }, '');

}

// 投稿から画像を取得
function getImagesFromPost(post) {
  const images = post.querySelectorAll(IMAGE_QUERY);
  return [].slice.call(images).map(e => ({
    url: e.src,
    alt: e.alt
  }));
}

// 投稿から画像/テキストどちらも取得して返す
function getBoth(post) {
  const message = getMessageFromPost(post);
  const image = getImagesFromPost(post);
  return {
    message,
    image,
  };
}

function sleep(msec) {
  return new Promise(function(resolve) {
    setTimeout(function() {resolve()}, msec);
  })
}

(function () {
  const posts = getPosts();
  const first = posts.map(getBoth);
  console.log('初回分');
  console.log(first);
  getFetchedPosts(async function(list) {
    await sleep(600);
    const added = list.map(post => getBoth(post));
    console.log('追加読み込み分');
    console.log(added);
  })

})();


