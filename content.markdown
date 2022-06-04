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
        <div class="col-3 content-list">
            <nav class="nav flex-column" id="menu">
            </nav>
        </div>
        <div class="col-9">
            <div class="row">
                <div class="col-6 d-flex justify-content-center">
                    <button class="btn content_btn" id="btn_original" onclick="show(0);">原文</button>
                </div>
                <div class="col-6 d-flex justify-content-center">
                    <button class="btn content_btn" id="btn_translated" onclick="show(1);">白話文</button>
                </div>
            </div>
            <br>
            <div class="row">
                <div class="card content-content">
                    <div class="card-body">
                        <h5 class="card-title placeholder-glow" id="card_title">
                            <span class="placeholder col-6"></span>
                        </h5>
                        <p class="card-text placeholder-glow" id="card_text_original">
                            <span class="placeholder col-5"></span>
                            <span class="placeholder col-8"></span>
                            <span class="placeholder col-6"></span>
                            <span class="placeholder col-2"></span>
                            <span class="placeholder col-9"></span>
                            <span class="placeholder col-2"></span>
                            <span class="placeholder col-7"></span>
                            <span class="placeholder col-2"></span>
                            <span class="placeholder col-9"></span>
                            <span class="placeholder col-6"></span>
                        </p>
                        <p class="card-text placeholder-glow" id="card_text_translated"></p>
                    </div>
                </div>
            </div>
        </div>
        <script>
            function change(Volumes, Articles){
                stmt = db.prepare("SELECT * FROM content where `Volumes` = " + Volumes + " and `Articles` = " + Articles + " order by Volumes, Articles");
                stmt.step();
                const result = stmt.getAsObject();
                document.getElementById('card_title').innerHTML = "第" + result['Volumes'] + "卷 > " + "第" + result['Articles'] + "篇 " + result['Name'];
                document.getElementById('card_text_original').innerHTML = result['Original'];
                document.getElementById('card_text_translated').innerHTML = result['Translated'];
                show(0);
            }
            function show(type) {
                if(type == 0) {
                    document.getElementById('card_text_original').style.display = "block";
                    document.getElementById('card_text_translated').style.display = "none";
					document.getElementById("btn_original").classList.remove("btn-outline-primary");
					document.getElementById("btn_original").classList.add('btn-primary');
					document.getElementById("btn_translated").classList.remove("btn-primary");
					document.getElementById("btn_translated").classList.add('btn-outline-primary');
                }
                else {
                    document.getElementById('card_text_original').style.display = "none";
                    document.getElementById('card_text_translated').style.display = "block";
					document.getElementById("btn_original").classList.remove('btn-primary');
					document.getElementById("btn_original").classList.add('btn-outline-primary');
					document.getElementById("btn_translated").classList.remove('btn-outline-primary');
					document.getElementById("btn_translated").classList.add('btn-primary');
                }
            }
            init().then(
                function (value) {
                    var select = document.getElementById('menu');
                    var stmt = db.prepare("SELECT * FROM content order by Volumes, Articles");
					num = 0;
                    while (stmt.step()) {
						const result = stmt.getAsObject();
						console.log(result['Volumes'] + " / " + result['Articles']);
						if(result['Volumes'] == 0){
							var1 = document.createElement('li');
							var1.classList.add('nav-item');
							var2 = document.createElement('a');
							var2.classList.add('nav-link');
							var2.addEventListener('click', function(){
								change(result['Volumes'], result['Articles']);
							});
							var2.innerHTML = "自序";
							var1.appendChild(var2);
							select.appendChild(var1);
							continue;
						}
						if(num != result['Volumes']){
							if(typeof li !== "undefined" && typeof a !== "undefined" && typeof ul !== "undefined"){
								li.appendChild(a);
								li.appendChild(ul);
								select.appendChild(li);
							}
							li = document.createElement('li');
							li.classList.add('nav-item');
							a = document.createElement('a');
							a.classList.add('nav-link');
							a.classList.add('dropdown-toggle');
							a.setAttribute("data-bs-toggle", "dropdown");
							a.setAttribute("role", "button");
							a.innerHTML = "第" + result['Volumes'] + "卷";
							ul = document.createElement('ul');
							ul.classList.add('dropdown-menu');
							num = result['Volumes'];
						}
						var1 = document.createElement('li');
                        var2 = document.createElement('a');
                        var2.classList.add('dropdown-item');
                        var2.innerHTML = "第" + result['Articles'] + "篇 - " + result['Name'];
                        var2.addEventListener('click', function(){
                            change(result['Volumes'], result['Articles']);
                        });
                        var1.appendChild(var2);
						ul.appendChild(var1);
                    }
					if(typeof li !== "undefined" && typeof a !== "undefined" && typeof ul !== "undefined"){
						li.appendChild(a);
						li.appendChild(ul);
						select.appendChild(li);
					}
					change(0,0);
                },
                function (error) {
                    window.alert("ERROR! Cannot init");
                }
            )
        </script>
    </div>
</div>
