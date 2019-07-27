Vue.component('favorite', {
    props: ['value'],
    template: `
        <li class="favorite list-inline-item">
            <h5><span class="badge badge-pill badge-info">{{ value }}</span></h5>
        </li>
    `
});

Vue.component('attention', {
    props: ['value'],
    template: `
        <li class="attention list-inline-item">
            <h5><span class="badge badge-pill badge-warning">{{ value }}</span></h5>
        </li>
    `
});

Vue.component('card', {
    props: ['title', 'type', 'level', 'abstract', 'imgPath'],
    template: `
    <div class="col-md-4">
        <div class="card mb-4 shadow">
            <div class="card-header bg-transparent p-0">
                <img v-bind:src="imgPath" class="card-img-top" height="140" alt="Квантовая теория поля" style="object-fit: cover;">
            </div>
            <div class="card-body">
                <h5 class="card-title">{{ title }}</h5>
                <div class="card-subtitle mb-2 text-muted">
                    <div class="d-flex justify-content-between align-items-center">
                        <h6 class="mb-0">{{ type }}</h6>
                        <h6 class="mb-0">{{ level }}</h6>
                    </div>
                </div>
                <p class="card-text mb-2">{{ abstract }}</p>
            </div>
            <div class="card-footer bg-transparent">
                <div class="d-flex justify-content-between align-items-center">
                    <p class="mb-0"><a href="#" class="text-warning" data-toggle="tooltip" data-placement="top" title="Добавить в избранное"><i class="fas fa-star fa-fw"></i></a></p>
                    <p class="mb-0"><a href="#" class="text-danger" data-toggle="tooltip" data-placement="top" title="Мне это не интересно"><i class="fas fa-times fa-fw"></i></a></p>
                </div>
            </div>
        </div>
    </div>
    `
});

var app = new Vue({
    el: '#app',
    data: {
        favorites: [],
        attentions: [],
        cards_favorites: [],
        cards_attentions: []
    },
    methods: {
        async getFavorites() {
            let response = await fetch('/api/favorites/');
            let json = await response.json();
            this.favorites = json.favorites;
        },
        async getAttentions() {
            let response = await fetch('/api/attentions/');
            let json = await response.json();
            this.attentions = json.attentions;
        },
        async getCardsFavorites() {
            let response = await fetch('/api/cards_favorites/');
            let json = await response.json();
            this.cards_favorites = json.cards_favorites;
        },
        async getCardsAttentions() {
            let response = await fetch('/api/cards_attentions/');
            let json = await response.json();
            this.cards_attentions = json.cards_attentions;
        }
    },
    created: function() {
        this.getFavorites();
        this.getAttentions();
        this.getCardsFavorites();
        this.getCardsAttentions();
    }
});