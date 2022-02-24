Vue.component('confirm-modal', {
    template: `
    <div>
        <b-modal id="confirmModal" hide-footer>
            <template #modal-title>
                {{title}}
            </template>
            <div class="d-block text-center">
                <p>{{message}}</p>
            </div>
            <b-row>
                <b-col class="text-center">
                    <b-button class="mt-3" @click="hide();">閉じる</b-button>
                </b-col>
            </b-row>
        </b-modal>
    <div>
    `,
    props: {
        title: String,
        message: String,
    },
    methods: {
        hide() {
            this.$bvModal.hide('confirmModal');
        }
    }
})