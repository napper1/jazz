<template>
    <b-modal ref="addSongModal"
             id="song-modal"
             title="Add a new song"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
                    label="Title:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addSongForm.title"
                        required
                        placeholder="Title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-artist-group"
                      label="Artist:"
                      label-for="form-artist-input">
            <b-form-input id="form-artist-input"
                          type="text"
                          v-model="addSongForm.artist"
                          required
                          placeholder="Artist">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-link-group" label="Link:" label-for="form-link-input">
            <b-form-input id="form-link-input" type="text" v-model="addSongForm.link" placeholder="YouTube link">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-category-group"
                        label="Category:"
                        label-for="form-artist-input">
            <b-form-select v-model="addSongForm.selected_category" :options="song_categories"></b-form-select>
          </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "AddSongModal",
        props: {
            song_categories: {
                type: Array,
                required: true,
            }
        },
        data(){
          return{
            addSongForm: {
              title: '',
              artist: '',
              link: '',
              selected_category: '',
            },
          }
        },
        methods: {
          onSubmit(evt) {
            evt.preventDefault();
            this.$refs.addSongModal.hide();
            const payload = {
              title: this.addSongForm.title,
              artist: this.addSongForm.artist,
              link: this.addSongForm.link,
              category: this.addSongForm.selected_category,
            };
            this.addSong(payload);
            this.initForm();
          },
          onReset(evt) {
            evt.preventDefault();
            this.$refs.addSongModal.hide();
            this.initForm();
          },
          addSong(payload) {
            const path = '/api-add-song/';
            axios.post(path, payload)
              .then(() => {
                this.$emit('refresh-songs', 'Song added!');
              })
              .catch((error) => {
                // eslint-disable-next-line
                console.log(error);
              });
          },
          initForm() {
            this.addSongForm.title = '';
            this.addSongForm.artist = '';
            this.addSongForm.link = '';
            this.addSongForm.selected_category = '';
          },
        }
    }
</script>

<style scoped>

</style>
