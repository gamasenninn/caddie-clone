Vue.component('sc-menu',{
    template: `  
    <div>
    <b-button v-b-toggle.sidebar-no-header>メニュー</b-button>
    <b-sidebar id="sidebar-no-header" aria-labelledby="sidebar-no-header-title" no-header shadow>
        <template #default="{ hide }">
            <div class="p-3">
                <h4 id="sidebar-no-header-title" style="float: left; width: 75%;">遷移メニュー</h4>
                <b-button variant="danger" block @click="hide" style="float: right; width: 15%;">✖
                </b-button>
                <b-img src="https://free-materials.com/adm/wp-content/uploads/2020/10/logo_07-1024x1024.png"
                    style="width: 50%; " center ></b-img>
                <nav class="mt-3">
                    <b-nav vertical class="mb-4">
                        <b-button variant="info" block href="/home-page"><i class="fas fa-home"></i>　TOP
                        </b-button>
                    </b-nav>
                    <b-nav vertical>
                        <b-button variant="primary" block href="/customer-page"><i
                                class="fas fa-building"></i>　得意先
                        </b-button>
                        <b-button variant="primary" block href="/item-page"><i class="fas fa-box"></i>　商　品
                        </b-button>
                        <b-button variant="primary" block href="/invoice-page"><i
                                class="fas fa-copy"></i>　請求書</b-button>
                        <b-button variant="primary" block href="/quotation-page"><i
                                class="far fa-copy"></i>　見積書</b-button>
                        <b-button variant="primary" block href="/memo-page"><i
                                class="fas fa-book-open"></i>　メ　モ</b-button>
                        <b-button variant="warning" block href="/login"><i
                                class="fas fa-book-open"></i>　ログイン</b-button>
                        <b-button variant="warning" block href="/logout"><i
                                class="fas fa-book-open"></i>　ログアウト</b-button>
                    </b-nav>
                </nav>
            </div>
        </template>
    </b-sidebar>
    </div>
    `,
    props: []
});