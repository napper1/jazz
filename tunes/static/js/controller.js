
var music_app = new Vue({
    el: '#music_app',
    data: {
        message: "Hello World!",
        artists: [],
        songs: [],
        selected_artist: "",
        artist: "",
        title: "",
        link: "",
        tags: "",
        letters: 'abcdefghijklmnopqrstuvwxyz'.toUpperCase().split(''),
        search_param: "",
        youtube_param: "",
        results: [],
        recently_added: [],
        recently_added_all: [],
        last_played: [],
        youtube_results: [],
        suggestions: [],
        open: false,
        current: 0,
        favourites: [],
    },
    created: function(){
        this.$http.get('/artists/').then(response => {
            // success callback
            this.data = response.body;
            this.artists = response.body;

        }, response => {
            // error callback
        });

        this.$http.get('/songs/?show=recent&limit=short').then(response => {
            this.recently_added = response.body;
        }, response =>{
           // error
        });
        this.$http.get('/songs/?show=recent').then(response => {
            this.recently_added_all = response.body;
        }, response =>{
           // error
        });

        this.get_last_played();
        this.get_favourites();

        this.$http.get('/music/suggestions/').then(response => {
                this.suggestions = response.body;
            });
    },
    computed: {
        //Filtering the suggestion based on the input
        matches: function() {
            return this.suggestions.filter((str) => {
                return str.indexOf(this.artist) >= 0;
            });
        },
        openSuggestion: function(){
            if (this.artist != "" &&
                this.open == true &&
                this.matches.length != 0){
                return 'open';
            };
        },
    },
    methods: {
        get_songs: function(artist){
            this.selected_artist = artist.name;
            this.$http.get('/songs/?artist=' + artist.id).then(response => {
                // success
                this.songs = response.body;
                console.log(response.body);
            }, response => {
                // error
            })
        },
        get_search_results: function(){
          this.$http.get('/songs/?q=' + this.search_param).then(response => {
              //success
              this.results = response.body;
        }, response => {
                // error
         })
        },
        get_artists_by_letter: function(letter){
            this.$http.get('/artists/?letter=' + letter).then(response => {
                this.artists = response.body;
            })
        },
        addSong: function(){
            this.$http.post('/music/api-add-song/',
                {artist: this.artist, title: this.title, link: this.link, tags: this.tags}).then(response => {
                // success
                var data = response.body;
                if (data.response == false){
                     $.growl.error({ message: "Something went wrong!" });
                }
                else{
                    $.growl({ title: "Song Added!", message: "Your song has been added." });
                }
            }, response => {
                // error
            })
        },
        updateStatus: function(song){
            console.log(song);

            this.$http.post('/music/api-update-last-played/' + song.id + '/', song).then(response => {
                // success
                $.growl({title: "Song modified.", message: " "});
                this.get_last_played();
            })
        },
        addFavourite: function(song){
            // update scope of song with is favourite
            song.is_favourite = true;
            this.$http.put('/songs/' + song.id + '/', song).then(response => {
                // success
                $.growl({title: "Favourite added!.", message: " "});
                this.get_favourites();
            })
        },
        get_last_played: function(){
            this.$http.get('/songs/?show=last_played').then(response => {
                // success
                this.last_played = response.body;
            })
        },
        get_favourites: function(){
            this.$http.get('/songs/?is_favourite=true').then(response => {
                // success
                this.favourites = response.body;
            })
        },
        search_youtube: function(){
            this.$http.get('/music/search_youtube/?name=' + this.youtube_param).then(response => {
                // success
                this.youtube_results = response.body;
                $('.thumbnail').matchHeight();
            }, response => {
                    // error
            })
        },
        suggestionClick: function(idx){
            this.artist = this.matches[idx];
            this.open = false;
        },
        changeSuggestion: function(){
            if (this.artist != ""){
                this.open = true;
            }
            else{
                this.open = false;
                this.current = 0;
            }
        },
        enterSuggestion: function(){
            this.artist = this.matches[this.current];
            this.open = false;
            this.current = 0;
        },
        upSuggestion: function(){
            if(this.current > 0)
                this.current--;
        },
        downSuggestion: function(){
            if(this.current < this.matches.length - 1)
                this.current++;
        },
        isActive: function(index) {
            return index === this.current;
        },
        save_yt_song: function(title, url){
            this.title = title;
        },
        downloadSong: function(song){
            this.$http.post('/music/download/' + song.id + '/').then(response => {
                // success
                $.growl({ title: "Song downloaded to media folder!",
                          message: "Your song has been converted to mp3 and in media folder." });

            }, response => {
                    // error
            })
        },
    },
   watch: {
        'search_param': function(val, oldVal){
         if (val && val !== oldVal) {
             this.get_search_results();
         }
         else{
            this.results = [];
         }
        }


    }

});

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment(String(value)).format('MM/DD/YYYY')
  }
});