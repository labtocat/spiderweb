<template>
  <div class="container">
    <header class="navbar">
      <section class="navbar-section">
        <a href="#" class="navbar-brand mr-2">SpiderWeb</a>
        <a href="#" class="btn btn-link">Docs</a>
        <a href="#" class="btn btn-link">GitHub</a>
      </section>
      <section class="navbar-section">
      </section>
    </header>
    <div class="container" style="margin-top:2%">
      <form  @submit.prevent="createCrawl()">
        <div class="columns">
          <div class="column col-4">
            <div class="form-group">
              <input class="form-input" type="text" id="input-url" v-model="spider.url"  placeholder="Type the url" required>
              <small>format should be https://website.com</small>
            </div>
          </div>
          <div class="column col-1">
            <div class="form-group">
              <input class="form-input" type="number" id="input-depth" v-model="spider.depth"  placeholder="depth" required>
            </div>
          </div>
          <div class="column col-2">
            <button class="btn btn-primary" type="submit">Crawl Web Page</button>
          </div>
        </div>
      </form>
      <br>
      <div class="columns" v-if="progress">
        <div class="column col-6">
          <span class="h2">crawling web pages...</span>
          <progress class="progress" max="100"></progress>
        </div>
        <div class="column col-6"></div>
      </div>

      <div class="columns" v-if="!images">
        <div class="column col-6">
          <span class="h2">no images found :(</span>
          <progress class="progress" max="100"></progress>
        </div>
        <div class="column col-6"></div>
      </div>

      <div class="columns" v-if="error">
        <div class="column col-6">
          <span class="h2">{{errorMsg.msg}} :(</span>
          <progress class="progress" max="100"></progress>
        </div>
        <div class="column col-6"></div>
      </div>

      <div v-if="images.length > 0">
        <span class="h2">Search results :)</span><br>
      </div>
      <div class="columns">
        <div class="accordion" v-for="item in images">
          <input type="checkbox" v-bind:id=item.level name="accordion-checkbox" hidden>
          <label class="accordion-header" v-bind:for=item.level>
            <i class="icon icon-arrow-right mr-1"></i>
            Level {{item.level}}
          </label>
          <div class="accordion-body" >
            <div class="column col-2" v-for="img in item.images" style="max-width:25%;float:left">
              <div class="card">
                <img :src=img class="img-responsive">
              </div>
            </div>
            <div v-if="item.images.length == 0">
              <p>no images found</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  data() {
    return {
      images: {},
      spider: {},
      progress: false,
      error: false
    };
  },

  methods: {
    createCrawl() {
      this.progress = true
      this.images = {}
      this.error = false
      this.errorMsg = ''
      axios
        .post("/search", {
          data: this.spider,
          headers: 'Content-Type: application/x-www-form-urlencoded'
        })
        .then(resp => {
          if (resp.status == 200){
            this.images = resp.data
          }else {
            this.progress = false
            this.error = true
            this.errorMsg = resp.data
          }
          this.progress = false
        })
        .catch(err => {
          this.progress = false
          this.error = true
        });
    }
  }
};
</script>
