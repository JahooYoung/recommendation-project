<template>
  <div class="home">
    <b-container>
      <b-row>
        <b-col cols="12" align="center">
          <h1>You may be intrested in</h1>
          <b-card-group
            v-if="movieRcmds.length > 0"
            columns
            class="mb-3"
          >
            <b-card
              v-for="movie in movieRcmds"
              :key="movie.movie.id"
              :title="movie.movie.title"
              tag="article"
              style="max-width: 20rem;"
            >
              <b-card-text>
                {{ movie.movie.genres.replace(/\|/g, ',') }}
              </b-card-text>
              <b-form-rating
                :value="movie.movie.meanRating"
                readonly
                class="mb-2"
              />
              <b-button
                :to="`/movies/${movie.movie.id}`"
                variant="primary"
                @click="send_rcmd_click"
              >
                See details
              </b-button>
            </b-card>
          </b-card-group>
          <b-link
            v-else
            to="/movies"
          >
            Ooops! Go and rate some movies!
          </b-link>
          <hr>
        </b-col>
        <b-col cols="12" align="center">
          <h1>Top 10</h1>
          <!-- <b-carousel
            :interval="4000"
            controls
            indicators
            background="#ababab"
            img-width="500"
            img-height="100"
            style="text-shadow: 1px 1px 2px #333;"
          >
            <b-carousel-slide
              v-for="movie in movieTop10"
              :key="movie.id"
              :caption="movie.title"
              img-src="https://m.media-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzI@._V1_UX400_CR0,0,400,589_AL_.jpg"
              @click="openLink(movie)"
            />
          </b-carousel> -->
          <b-card-group
            v-for="movieGroup in movieTop10Grouped"
            :key="`card-group-${movieGroup[0].id}`"
            columns
            class="mb-3"
          >
            <b-card
              v-for="movie in movieGroup"
              :key="movie.id"
              :title="movie.title"
              tag="article"
              style="max-width: 20rem;"
            >
              <b-card-text>
                {{ movie.genres.replace(/\|/g, ',') }}
              </b-card-text>
              <b-form-rating
                :value="movie.meanRating"
                readonly
                class="mb-2"
              />
              <b-button
                :to="`/movies/${movie.id}`"
                variant="primary"
              >
                See details
              </b-button>
            </b-card>
          </b-card-group>
        </b-col>
      </b-row>
    </b-container>
    <!-- <b-container>
      <b-row>
        <b-col
          v-if="user !== null"
          cols="12"
          order="1"
          lg="4"
          order-lg="1"
          align="center"
        >
          <b-card
            no-body
            :header="$t('Your Recently Edited Notes')"
            class="mb-3"
            border-variant="dark"
            header-bg-variant="dark"
            header-text-variant="white"
          >
            <b-list-group flush>
              <b-list-group-item
                v-for="note in userRecentNotes"
                :key="'recent-note-' + note.id"
                :to="'/note/' + note.id"
                class="d-flex justify-content-between align-items-center"
              >
                {{ note.title }}
                <small>{{ note.lastModified.toLocaleString() }}</small>
              </b-list-group-item>
            </b-list-group>
          </b-card>

          <b-button
            v-b-modal.new-note-modal
            pill
            variant="outline-dark"
          >
            <b-icon icon="plus"></b-icon>
            New Note
          </b-button>
        </b-col>
        <b-col
          cols="12"
          order="1"
          lg="2"
          order-lg="1"
          v-else
        />

        <b-col
          cols="12"
          order="1"
          lg="8"
          order-lg="2"
        >
          <h3>{{ 'Recently Updated Notes' }}</h3>
          <div
            v-for="note in recentNotes"
            :key="'recent-note-' + note.id"
            no-body
            class="my-4"
          >
            <h4 class="mb-2">
              <b-link
                :to="`/note/${note.id}`"
                active-class=""
                exact-active-class=""
              >
                {{ note.title }}
              </b-link>
            </h4>
            <div class="d-flex w-100 justify-content-between">
              <p> by {{ note.owner.username }} </p>
              <em>last modified at {{ note.lastModified.toLocaleString() }}</em>
            </div>
            <p
              class="mb-2"
              style="text-align: left"
            >
              {{ note.abstract }}
            </p>
            <hr>
          </div>
        </b-col>
      </b-row>
    </b-container> -->
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Home',
  data() {
    return {
      movieTop10: [],
      movieRcmds: [],
    }
  },
  computed: {
    movieTop10Grouped() {
      const batch = 10
      const result = []
      for (let i = 0; i < this.movieTop10.length; i += batch) {
        result.push(this.movieTop10.slice(i, i + batch))
      }
      return result
    }
  },
  created () {
    this.fetchData()
  },
  watch: {
    user() {
      this.fetchData()
    }
  },
  methods: {
    async fetchData() {
      const res = await this.axios.get(`/api/movies/`, {
        params: {
          limit: 10,
          total_rating__gte: 300,
          ordering: '-mean_rating'
        }
      })
      this.movieTop10 = res.data.results
      if (this.user !== null) {
        const res = await this.axios.get(`/api/movie-rcmds/`, {
          params: {
            limit: 10,
            ordering: '-rating'
          }
        })
        this.movieRcmds = res.data.results
      }
      // if (this.user !== null) {
      //   const res1 = await this.axios.get(`/api/documents/`, {
      //     params: {
      //       limit: 5,
      //       owner__username: this.user,
      //       ordering: '-last_modified'
      //     }
      //   })
      //   this.userRecentNotes = res1.data.results
      // } else {
      //   this.userRecentNotes = []
      // }
      // const res = await this.axios.get(`/api/documents/`, {
      //   params: {
      //     ordering: '-last_modified'
      //   }
      // })
      // this.recentNotes = res.data.results
    },
    openLink(movie) {
      const url = `https://www.imdb.com/title/tt${String(movie.imdbId).padStart(7, '0')}/`
      window.open(url, '_blank')
    },
    async send_rcmd_click() {
      await this.axios.post('/api/kafka/', {
        is_rcmd: true
      })
    }
  }
}
</script>
