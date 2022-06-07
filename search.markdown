---
layout: default
title: 搜尋
---

<script src="https://cdnjs.cloudflare.com/ajax/libs/feather-icons/4.29.0/feather.min.js"
    integrity="sha512-24XP4a9KVoIinPFUbcnjIjAjtS59PUoxQj3GNVpWc86bCqPuy3YxAcxJrxFCxXe4GHtAumCbO2Ze2bddtuxaRw=="
    crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.6.2/sql-wasm.min.js"
    integrity="sha512-7bKBIIhC5ktPKnC82Q257bDXW84tc9L5y318qySCidwScxOW1UCgi2aelmWAP3MWAURoKvA+n6G7FZaERDtYIg=="
    crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script>
    var db = null;
    async function init() {
        const sqlPromise = initSqlJs({
            locateFile: file => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.6.2/sql-wasm.wasm`
        });
        const dataPromise = fetch("/NTCU-GeneralEducation-WisdomOfClassics/assets/db/database.sqlite").then(res => res.arrayBuffer());
        const [SQL, buf] = await Promise.all([sqlPromise, dataPromise]);
        db = new SQL.Database(new Uint8Array(buf));
    }
    init();
    function search() {
        search_text = document.getElementById("search_text").value;
        document.getElementById("result").innerHTML = "";
        if (search_text.length < 2) {
            document.getElementById("status").innerHTML = "請輸入2個字以開始搜尋";
        }
        else {
            from_name = document.getElementById('search-from_name').checked;
            from_original = document.getElementById('search-from_original').checked;
            from_translated = document.getElementById('search-from_translated').checked;
            stmt = db.prepare("SELECT * FROM content where " + from_name + " and `Name` LIKE '%" + search_text + "%' or " + from_original + " and `Original` LIKE '%" + search_text + "%' or " + from_translated + " and `Translated` LIKE '%" + search_text + "%'");
            count = 0;
            while (stmt.step()) {
                count += 1;
                const result = stmt.getAsObject();
                accordion_item = document.createElement('div');
                accordion_item.classList.add('accordion-item');
                accordion_header = document.createElement('h2');
                accordion_header.classList.add('accordion-header');
                accordion_button = document.createElement('button');
                accordion_button.classList.add('accordion-button');
                accordion_button.setAttribute("type", "button");
                accordion_button.setAttribute("data-bs-toggle", "collapse");
                accordion_button.setAttribute("data-bs-target", "#collapse" + count);
                accordion_button.innerHTML = "第" + result['Volumes'] + "卷 - 第" + result['Articles'] + "篇 " + result['Name'];
                accordion_header.appendChild(accordion_button);
                accordion_item.appendChild(accordion_header);
                accordion_collapse = document.createElement('div');
                accordion_collapse.id = "collapse" + count;
                accordion_collapse.classList.add('accordion-collapse');
                accordion_collapse.classList.add('collapse');
                if (count == 1)
                    accordion_collapse.classList.add('show');
                accordion_collapse.setAttribute("data-bs-parent", "#result");
                accordion_body = document.createElement('div');
                accordion_body.classList.add('accordion-body');
                container = document.createElement('div');
                container.classList.add('container');
				row1 = document.createElement('div');
				row1.classList.add('row');
				col1 = document.createElement('div');
				col1.classList.add('col');
				col1.classList.add('border');
				col1.classList.add('text-center');
				col1.classList.add('fw-bold');
                col1.innerHTML = "原文";
				row1.appendChild(col1);
				col2 = document.createElement('div');
				col2.classList.add('col');
				col2.classList.add('border');
				col2.classList.add('text-center');
				col2.classList.add('fw-bold');
                col2.innerHTML = "翻譯";
				row1.appendChild(col2);
				container.appendChild(row1);
                row2 = document.createElement('div');
                row2.classList.add('row');
                col3 = document.createElement('div');
                col3.classList.add('col');
                col3.classList.add('border');
                col3.innerHTML = result['Original'];
                row2.appendChild(col3);
                col4 = document.createElement('div');
                col4.classList.add('col');
                col4.classList.add('border');
                col4.innerHTML = result['Translated'];
                row2.appendChild(col4);
                container.appendChild(row2);
                accordion_body.appendChild(container);
                accordion_collapse.appendChild(accordion_body);
                accordion_item.appendChild(accordion_collapse);
                document.getElementById("result").appendChild(accordion_item);
            }
            document.getElementById("status").innerHTML = "搜尋結束，共找到 " + count + " 筆結果";
        }
    }
</script>

<div class="container-lg">
    <div class="input-group mb-3">
        <span class="input-group-text">
            <i data-feather="search"></i>
            <script>
                feather.replace()
            </script>
        </span>
        <input type="text" class="form-control" id="search_text" oninput="search()" placeholder="輸入關鍵字開始搜尋 (EX. 飲酒)">
    </div>
    <label class="col-form-label">搜尋範圍</label>
    <div class="form-check form-check-inline form-switch">
        <input class="form-check-input" type="checkbox" role="switch" id="search-from_name" onchange="search()" checked>
        <label class="form-check-label" for="search-from_name">名稱</label>
    </div>
    <div class="form-check form-check-inline form-switch">
        <input class="form-check-input" type="checkbox" role="switch" id="search-from_original" onchange="search()" checked>
        <label class="form-check-label" for="search-from_original">原文</label>
    </div>
    <div class="form-check form-check-inline form-switch">
        <input class="form-check-input" type="checkbox" role="switch" id="search-from_translated" onchange="search()">
        <label class="form-check-label" for="search-from_-translated">譯文</label>
    </div>

    <div>
        <div id="status">請輸入2個字以開始搜尋</div>
        <div class="accordion" id="result"></div>
    </div>
</div>