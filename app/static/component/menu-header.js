Vue.component('menu-header', {
    template: `
    <div>
        <b-card class="fixed-top header" style="background: rgba(255,255,255,0.5);">
            <b-row>
                <b-col></b-col>
                <b-col cols="11">
                    <b-row>
                        <b-col>
                            <router-link to="?page=store">
                                <b-button pill variant="success" class="mr-3" @click="mainAddRow();">＋新規作成
                                </b-button>
                            </router-link>
                        </b-col>
                        <b-col class="text-right">
                            <sc-menu v-if="modeName!='mw'"></sc-menu>
                        </b-col>
                    </b-row>
                </b-col>
                <b-col></b-col>
            </b-row>
        </b-card>
    </div>
    `,
    props: {
        mainAddRow: Function,
    },
    methods: {
        modeName: function () {
            return localStorage.getItem('wMode');
        },
    },
})