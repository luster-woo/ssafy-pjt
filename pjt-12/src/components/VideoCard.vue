<template>
  <div class="card h-100" @click="open">
    <div style="position:relative">
      <img :src="thumb" class="card-img-top" alt="thumb" />
    </div>
    <div class="card-body">
      <h5 class="card-title text-truncate" title="{{ title }}">{{ title }}</h5>
      <p class="card-text text-muted small">{{ channel }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: { video: { type: Object, required: true } },
  computed: {
    id() { return this.video.id.videoId },
    thumb() { return this.video.snippet.thumbnails.medium.url },
    title() { return this.video.snippet.title },
    channel() { return this.video.snippet.channelTitle }
  },
  methods: {
    open() { this.$router.push(`/video/${this.id}`) }
  }
}
</script>

<style>
.card{cursor:pointer;border:1px solid #ddd;padding:8px;border-radius:6px;background:#fff}
.card img{width:100%;height:120px;object-fit:cover}
.card h3{font-size:14px;margin:8px 0}
.channel{color:#666;font-size:12px}
</style>
