<template>
  <el-form
    ref="lessonVideoSelect"
    v-loading="loading"
    size="small"
    style="margin-top: -30px"
    @submit.native.prevent
  >
    <el-form-item>
      <el-table
        v-loading="tableLoading"
        class="videos-table"
        :data="tableData"
        highlight-current-row
        @current-change="currentRowChange"
      >
        <template slot="empty">
          <template v-if="!tableLoading">
            没有符合条件的记录
          </template>
          <template v-else>
            &nbsp;
          </template>
        </template>
        <el-table-column
          width="50"
          align="right"
        >
          <template v-slot="scope">
            <el-radio
              v-if="currentRow !== null && scope['row']['id'] === currentRow['id']"
            />
          </template>
        </el-table-column>
        <el-table-column
          label="视频"
          width="140"
        >
          <template v-slot="scope">
            <el-image
              :src="scope['row']['cover']"
              class="cover-img"
            />
          </template>
        </el-table-column>
        <el-table-column>
          <template v-slot="scope">
            <div>{{ scope.row['title'] }}</div>
            <div style="color: #909399; font-size: 12px">
              {{ scope.row['duration'] }}
            </div>
          </template>
        </el-table-column>
        <el-table-column
          prop="creation_time"
          label="创建时间"
        />
      </el-table>
      <el-pagination
        layout="total, sizes, prev, pager, next"
        :pager-count="5"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        :page-size.sync="pageSize"
        :current-page="currentPage"
        @size-change="refreshData"
        @current-change="pullData"
      />
    </el-form-item>
    <el-form-item class="submit-container">
      <div class="video-id">
        {{ currentRow !== null ? `ID: ${currentRow['id']}` : '&nbsp;' }}
      </div>
      <el-button
        type="primary"
        native-type="submit"
        :disabled="currentRow === null"
        @click="onSubmit"
      >
        提交
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LessonVideoSelect',
  props: {
    slug: {
      type: String,
      required: true,
    },
    id: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      tableData: [],
      currentRow: null,
      currentPage: 1,
      pageSize: 10,
      total: 0,
      loading: false,
      tableLoading: false,
      cancel: null,
    }
  },
  mounted() {
    this.pullData()
  },
  methods: {
    refreshData() {
      this.tableData = []
      this.currentPage = 1
      this.total = 0
      this.pullData()
    },
    pullData() {
      this.tableLoading = true
      if (this.cancel !== null) {
        this.cancel()
        this.cancel = null
      }
      this.$axios.get('/videos', {
        cancelToken: new axios.CancelToken((c) => {
          this.cancel = c
        }),
        params: {
          page_no: this.currentPage,
          limit: this.pageSize
        }
      }).then((response) => {
        this.total = response.data['count']
        this.tableData = response.data['results']
      }).catch((error) => {
        if (!axios.isCancel(error)) {
          this.tableData = []
          this.total = 0
          this.$message.error('无法连接到服务器，请检查网络后重试！')
        }
      }).then(() => {
        this.cancel = null
        this.tableLoading = false
      })
    },
    currentRowChange(value) {
      this.currentRow = value;
    },
    onSubmit() {
      if (this.currentRow !== null && !this.loading) {
        this.loading = true
        this.$axios.patch(`/course/${this.slug}/lesson/${this.id}`, {
          video_id: this.currentRow['id'],
        }).then((response) => {
          this.$message.success('成功选取视频！')
          this.$emit('success', response.data)
        }).catch(() => {
          this.$message.error('无法连接到服务器，请检查网络后重试！')
        }).then(() => {
          this.loading = false
        })
      }
    },
  },
}
</script>

<style scoped>
  .cover-img {
    width: 120px;
    display: block;
  }

  .submit-container {
    text-align: center;
  }

  .videos-table >>> tbody tr {
    cursor: pointer;
  }

  .video-id {
    font-size: 12px;
    color: rgba(0, 0, 0, 0.2);
    margin-bottom: 10px;
  }
</style>