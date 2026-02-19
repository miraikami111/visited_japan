var infoData = __INFO_JSON__;

  function openModal(pref) {
    var data = infoData[pref] || {};
    var imgs = data.images || [];
    var text = data.text || "";
    var tags = data.tags || [];

    var old = document.getElementById('modal');
    if (old) old.remove();

    var modal = document.createElement('div');
    modal.id = 'modal';
    modal.style.position = 'fixed';
    modal.style.inset = '0';
    modal.style.backgroundColor = 'rgba(0,0,0,0.8)';
    modal.style.display = 'flex';
    modal.style.justifyContent = 'center';
    modal.style.alignItems = 'center';
    modal.style.zIndex = '10000';

    var content = document.createElement('div');
    content.style.backgroundColor = 'white';
    content.style.padding = '12px';
    content.style.maxWidth = '900px';
    content.style.width = '90%';
    content.style.maxHeight = '85%';
    content.style.overflow = 'auto';
    content.style.borderRadius = '10px';

    var title = document.createElement('h2');
    title.textContent = pref;
    title.style.margin = '0 0 10px 0';
    content.appendChild(title);

    if (tags.length > 0) {
      var tagDiv = document.createElement('div');
      tagDiv.textContent = tags.join(' ');
      tagDiv.style.color = '#666';
      tagDiv.style.fontSize = '12px';
      tagDiv.style.margin = '0 0 8px 0';
      content.appendChild(tagDiv);
    }

    var closeBtn = document.createElement('button');
    closeBtn.textContent = '閉じる';
    closeBtn.onclick = function() { modal.remove(); };
    closeBtn.style.marginBottom = '10px';
    content.appendChild(closeBtn);

    if (imgs.length > 0) {
      var index = 0;
      var imgTag = document.createElement('img');
      imgTag.src = imgs[0];
      imgTag.style.width = '100%';
      imgTag.style.maxHeight = '55vh';
      imgTag.style.objectFit = 'contain';
      imgTag.style.background = '#111';
      imgTag.style.borderRadius = '8px';
      content.appendChild(imgTag);

      if (imgs.length > 1) {
        var nextBtn = document.createElement('button');
        nextBtn.textContent = '次の写真';
        nextBtn.style.marginTop = '8px';
        nextBtn.onclick = function() {
          index = (index + 1) % imgs.length;
          imgTag.src = imgs[index];
        };
        content.appendChild(nextBtn);
      }
    } else {
      var noImg = document.createElement('div');
      noImg.textContent = '(写真なし)';
      noImg.style.color = '#666';
      content.appendChild(noImg);
    }

    var p = document.createElement('p');
    p.textContent = text || '';
    p.style.marginTop = '10px';
    content.appendChild(p);

    modal.addEventListener('click', function(e) {
      if (e.target === modal) modal.remove();
    });

    modal.appendChild(content);
    document.body.appendChild(modal);
  }

  function renderResult(pref) {
    var images = (infoData[pref] && infoData[pref].images) || [];
    var tags = (infoData[pref] && infoData[pref].tags) || [];
    var imgHtml = "";
    if (images.length > 0) {
      imgHtml = '<img src="' + images[0] + '" style="width:60px;height:auto;border-radius:6px;">';
    }
    return (
      '<div style="display:flex;align-items:center;gap:8px;">' +
        imgHtml +
        '<div>' +
          '<div style="font-weight:bold;">' + pref + '</div>' +
          '<div style="font-size:12px;color:#666;">' + tags.join(' ') + '</div>' +
        '</div>' +
      '</div>'
    );
  }

  document.addEventListener("DOMContentLoaded", function() {
    var input = document.getElementById("tagInput");
    var resultsDiv = document.getElementById("searchResults");
    if (!input || !resultsDiv) return;

    input.addEventListener("input", function() {
      var query = (input.value || "").trim();
      resultsDiv.innerHTML = "";
      if (!query) return;

      // # はあってもなくてもOK
      query = query.replace(/^#/, "").toLowerCase();

      Object.keys(infoData || {}).forEach(function(pref) {
        var tags = (infoData[pref] && infoData[pref].tags) || [];
        var hit = tags.some(function(t) {
          return String(t).toLowerCase().replace(/^#/, "").includes(query);
        });

        if (hit) {
          var div = document.createElement("div");
          div.className = "resultItem";
          div.innerHTML = renderResult(pref);
          div.onclick = function() { openModal(pref); };
          resultsDiv.appendChild(div);
        }
      });
    });
  });