<template>
  <b-container>
    <b-row>
      <b-col v-if="movie" align="center">
        <h1>
          {{ movie.title }}
        </h1>
        <div>
          <p> {{ movie.genres.replace(/\|/g, ',') }} </p>
        </div>
        <div>
          <b-form-rating
            :value="movie.meanRating"
            readonly
            class="mb-2"
          />
        </div>
        <b-link
          :href="`https://www.imdb.com/title/tt${String(movie.imdbId).padStart(7, '0')}/`"
          target="_blank"
        >
          Go to IMDB {{ movie.imdbId }}
        </b-link>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>

export default {
  name: 'NoteEdit',
  components: {
    // Editor
  },
  data() {
    return {
      movie: null,
    }
  },
  created () {
    this.fetchData()
  },
  watch: {
    $route() {
      this.fetchData()
    }
  },
  // beforeRouteUpdate(...args) {
  //   this.$refs.editor.beforeRouteUpdate(...args)
  // },
  // beforeRouteLeave(...args) {
  //   this.$refs.editor.beforeRouteLeave(...args)
  // }
  methods: {
    async fetchData() {
      const res = await this.axios.get(`/api/movies/${this.$route.params.id}/`)
      this.movie = res.data
    }
  }
}
</script>
