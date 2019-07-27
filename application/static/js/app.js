Vue.component('favorite', {
    props: ['id', 'value'],
    template: `
        <li>
            <div class="favorite">
                {{ value }}
            </div>
        </li>
    `
});

Vue.component('attention', {
    props: ['id', 'value'],
    template: `
        <li>
            <div class="attention">
                {{ value }}
            </div>
        </li>
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