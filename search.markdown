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
            stmt = db.prepare("SELECT * FROM content where `Original` LIKE '%" + search_text + "%'");
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
                row = document.createElement('div');
                row.classList.add('row');
                col1 = document.createElement('div');
                col1.classList.add('col');
                col1.classList.add('border');
                col1.innerHTML = result['Original'];
                row.appendChild(col1);
                col2 = document.createElement('div');
                col2.classList.add('col');
                col2.classList.add('border');
                col2.innerHTML = result['Translated'];
                row.appendChild(col2);
                container.appendChild(row);
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
        <input type="text" class="form-control" id="search_text" oninput="search()">
    </div>

    <div>
        <div id="status">請輸入2個字以開始搜尋</div>
        <div class="accordion" id="result"></div>
    </div>
</div>