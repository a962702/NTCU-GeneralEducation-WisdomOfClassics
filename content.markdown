---
layout: default
title: 內容
---

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
</script>
<div class="container">
    <div class="row">
        <div class="col-4" id="menu"></div>
        <script>
            function change(Volumes, Articles){
                stmt = db.prepare("SELECT * FROM content where `Volumes` = " + Volumes + " and `Articles` = " + Articles + " order by Volumes, Articles");
                stmt.step();
                const result = stmt.getAsObject();
                document.getElementById('card_title').innerHTML = result['Name'];
                document.getElementById('card_text_original').innerHTML = result['Original'];
                document.getElementById('card_text_translated').innerHTML = result['Translated'];
            }
            function show(type) {
                if(type == 0) {
                    document.getElementById('card_text_original').style.display = "block";
                    document.getElementById('card_text_translated').style.display = "none";
                }
                else {
                    document.getElementById('card_text_original').style.display = "none";
                    document.getElementById('card_text_translated').style.display = "block";
                }
            }
            init().then(
                function (value) {
                    var select = document.getElementById('menu');
                    var stmt = db.prepare("SELECT * FROM content order by Volumes, Articles");
                    while (stmt.step()) {
                        var opt = document.createElement('p');
                        const result = stmt.getAsObject();
                        opt.innerHTML = "第" + result['Volumes'] + "章 - 第" + result['Articles'] + "篇 - " + result['Name'];
                        opt.addEventListener('click', function(){
                            change(result['Volumes'], result['Articles']);
                        });
                        select.appendChild(opt);
                    }
                },
                function (error) {
                    window.alert("ERROR! Cannot init");
                }
            )
        </script>
        <div class="col-8">
            <div class="row">
                <div class="col-6 d-flex justify-content-center">
                    <button class="btn btn-outline-primary" id="btn_original" onclick="show(0);">原文</button>
                </div>
                <div class="col-6 d-flex justify-content-center">
                    <button class="btn btn-outline-primary" id="btn_translated" onclick="show(1);">白話文</button>
                </div>
            </div>
            <div class="row">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title" id="card_title"></h5>
                        <p class="card-text" id="card_text_original"></p>
                        <p class="card-text" id="card_text_translated"></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
