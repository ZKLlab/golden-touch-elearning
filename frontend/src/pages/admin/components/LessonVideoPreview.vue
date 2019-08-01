<template>
  <div>
    <video
      ref="videoPlayer"
      class="video"
    >
      <!---->
    </video>
  </div>
</template>

<script>
import Plyr from 'plyr'
import 'plyr/dist/plyr.css'
import i18n from '../../../plyr-i18n'

export default {
  name: 'LessonVideoPreview',
  props: {
    videoId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      player: null,
    }
  },
  mounted() {
    this.initVideo()
  },
  beforeDestroy() {
    this.destroyVideo()
  },
  methods: {
    initVideo() {
      this.$axios.get('/play_info', {
        params: {
          video_id: this.videoId,
        },
      }).then((response) => {
        let sources = []
        response.data['PlayInfoList']['PlayInfo'].forEach((value) => {
          sources.push({
            src: value['PlayURL'],
            type: `${value['StreamType']}/${value['Format']}`,
            size: value['Height'],
          })
        })
        this.player = new Plyr(this.$refs['videoPlayer'], {
          quality: {default: 540, options: [1080, 720, 540, 360]},
          ratio: '16:9',
          controls: ['play-large', 'play', 'progress', 'current-time', 'duration', 'mute', 'volume', 'captions', 'settings', 'download', 'fullscreen'],
          i18n: i18n,
        })
        this.player.source = {
          type: 'video',
          sources: sources,
          poster: response.data['VideoBase']['Cover'],
        }

      }).catch(() => {
        this.$message.error('视频加载失败，请重试……')
      })
    },
    destroyVideo() {
      if (this.player !== null) {
        this.player.destroy()
        this.player = null
      }
    },
  },
}
</script>

<style scoped>
  .video {
    width: 100%;
  }
</style>