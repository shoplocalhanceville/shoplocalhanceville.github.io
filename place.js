/* Click-to-load Facebook Page Plugin. Nothing loads from Facebook until the visitor asks. */
document.addEventListener('click',function(ev){var b=ev.target.closest&&ev.target.closest('.fb-load');if(!b)return;
var box=b.parentNode,href=box.getAttribute('data-href');if(!/^https:\/\/(www\.)?facebook\.com\//.test(href))return;
var w=Math.min(500,box.clientWidth||500),f=document.createElement('iframe');
f.src='https://www.facebook.com/plugins/page.php?href='+encodeURIComponent(href)+'&tabs=timeline&width='+w+'&height=600&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false';
f.title='Latest Facebook posts';f.loading='lazy';f.setAttribute('allow','encrypted-media');f.width=w;f.height=600;box.replaceChildren(f);});
