"use strict";

const POST_QUERY = '.userContentWrapper';
const MESSAGE_QUERY = '.userContent';
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

function getPosts(_target, _query) {
  const target = _target || document.getElementById('contentArea');
  const query = _query || POST_QUERY;
  const posts = target.nodeType === 1 ? target.querySelectorAll(query) : [];
  return [].slice.call(posts);
}

function getMessageFromPost(post) {
  const messages = post.querySelectorAll(MESSAGE_QUERY);
  return [].slice.call(messages).reduce((acc, message) => {
    console.log(message, message.innerHTML);
    return acc + message.innerHTML
  }, '');

}

function getImagesFromPost(post) {
  const images = post.querySelectorAll(IMAGE_QUERY);
  return [].slice.call(images).map(e => ({
    url: e.src,
    alt: e.alt
  }));
}


(function () {
  console.log('Hello, friend.');
  const posts = getPosts();
  // console.log(posts);
  const messages = posts.map(post => getMessageFromPost(post));
  const images = posts.map(post => getImagesFromPost(post));
  console.log(messages, images);

  getFetchedPosts(function(list) {
    const messages = list.map(post => getMessageFromPost(post));
    const images = list.map(post => getImagesFromPost(post));
    console.log(messages, images);
  })
})();


