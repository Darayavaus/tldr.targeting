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
    props: ['card'],
    template: `
    <div class="col-md-4">
        <h5 v-if="card.isAttention"><span class="badge badge-warning">Для успеваемости</span></h5>
        <h5 v-else><span class="badge badge-info">По интересам</span></h5>
        <div class="card mb-4 shadow">
            <div class="card-header bg-transparent p-0">
                <img v-bind:src="card.imgSrc" class="card-img-top" height="140" alt="Квантовая теория поля" style="object-fit: cover;">
            </div>
            <div class="card-body">
                <h5 class="card-title">{{ card.title }}</h5>
                <div class="card-subtitle mb-2 text-muted">
                    <div class="d-flex justify-content-between align-items-center">
                        <h6 class="mb-0">{{ card.type }}</h6>
                        <h6 class="mb-0">{{ card.level }}</h6>
                    </div>
                </div>
                <p class="card-text mb-2">{{ card.description }}</p>
            </div>
            <div class="card-footer bg-transparent">
                <div class="d-flex justify-content-between align-items-center">
                    <button type="button" v-on:click="favorCard(card.id)" class="btn btn-outline text-success p-0" data-toggle="tooltip" data-placement="top" title="Добавить в избранное">
                        <i class="fas fa-bookmark fa-fw" v-if="this.isFavorite || (card.id==23941 && card.isHackFavorite)"></i>
                        <i class="far fa-bookmark fa-fw" v-else></i>
                    </button>
                    <p class="mb-0"><i class="fas fa-star fa-fw text-muted"></i> {{ card.score }}</p>
                    <button type="button" v-on:click="removeCard(card.id)" class="btn btn-outline text-danger p-0" data-toggle="tooltip" data-placement="top" title="Мне это не интересно">
                        <i class="fas fa-times fa-fw"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>
    `,
    methods: {
        removeCard(cardId) {
            for (var i = 0; i < app.cards.length; i++) {
                if (app.cards[i].id == cardId) {
                    for (var j = 0; j < app.favorites.length; j++) {
                        if (app.favorites[j] == app.cards[i].theme) {
                            app.favorites.splice(j, 1);
                            break;
                        }
                    }
                    app.cards.splice(i, 1);
                }
            };
            // app.getCards();
        },
        favorCard() {
            this.isFavorite = !this.isFavorite;
            if (this.isFavorite) {
                app.favorites.push(this.card.theme);
                app.favoritesIndexes.push(this.card.kes);
            } 
            if (!this.isFavorite) {
                for (var i = 0; i < app.favorites.length; i++) {
                    if (app.favorites[i] == this.card.theme) {
                        app.favorites.splice(i, 1);
                        break;
                    }
                }
            }
        }
    },
    data() {
        return {
            isFavorite: false,
        };
    }
});

var app = new Vue({
    el: '#app',
    data: {
        favorites: [],
        favoritesIndexes: [],
        attentions: [],
        cards: []
    },
    watch: {
        favoritesIndexes: function (newIndexed, oldIndexes) {
            this.cards = [];
            this.getCards();
            // this.cards[3].isHackFavorite = true;
            // console.log(this.cards[3]);
        }
    },
    methods: {
        async getFavorites() {
            let response = await fetch('/api/favorites/');
            let json = await response.json();
            this.favorites = json.favorites.names;
            this.favoritesIndexes = json.favorites.indexes;
        },
        async getAttentions() {
            let response = await fetch('/api/attentions/');
            let json = await response.json();
            this.attentions = json.attentions;
        },
        async getCards() {
            let response = await fetch('/api/cards_attentions/');
            let json = await response.json();
            for(var i = 0; i < json.cards_attentions.length; i++) {
                json.cards_attentions[i].isAttention = true;
            };
            this.cards = json.cards_attentions;

            response = await fetch('/api/cards_favorites/' + this.parseFavoritesIdexes(this.favoritesIndexes));
            json = await response.json();
            for(var i = 0; i < json.cards_favorites.length; i++) {
                json.cards_favorites[i].isAttention = false;
            };
            this.cards = this.cards.concat(json.cards_favorites);
        },
        parseFavoritesIdexes(indexes) {
            return indexes.join('c');
        }
    },
    created: function() {
        this.getFavorites();
        this.getAttentions();
    }
});