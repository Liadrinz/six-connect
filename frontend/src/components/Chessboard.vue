<template>
    <div>
        <div class="mesh board">
            <div v-for="(i, idx) in range(x - 1)" :key="idx">
                <div class="cell square" v-for="(j, jdx) in range(y - 1)" :key="jdx"></div>
            </div>
        </div>
        <div class="play board">
            <div v-for="(i, idx) in range(x)" :key="idx">
                <div class="cell cross" v-for="(j, jdx) in range(y)" :key="jdx" @click="take(i, j, 1)"><span class="piece">{{getPiece(i, j)}}</span></div>
            </div>
        </div>
    </div>
</template>

<script>
import takeAlgorithm from '@/algorithm';

export default {
    name: 'Chessboard',
    props: {
        x: Number,
        y: Number,
        personColor: Number
    },
    created () {
        this.init();
    },
    data () {
        return {
            machineColor: 1 - this.personColor,
            colorToPiece: {
                0: '🌑',
                1: '⚪'
            },
            boardData: [],
            canTake: 1 - this.personColor,
        }
    },
    methods: {
        init() {
            this.boardData = [];
            for (let i = 0; i < this.x; ++i) {
                let row = [];
                for (let j = 0; j < this.y; ++j) {
                    row.push(-1);
                }
                this.boardData.push(row);
            }
            if (!this.canTake) this.machineTake();
        },
        // 构建传入父组件的数据
        createEventData(i, j, role) {
            return {
                board: this.boardData,
                change: [i, j, role]
            }
        },
        // 棋盘变化时调用父组件传入的回调函数并回传数据
        callbackOnChange() {
            this.$emit('change', this.boardData);
        },
        // 获取[0, N)的数组序列
        range(N) {
            return [...Array(N).keys()]
        },
        getPiece(i, j) {
            return this.boardData[i][j];
        },
        // 机器下棋的方法
        machineTake() {
            let [rx, ry] = takeAlgorithm(this.boardData);
            this.take(rx, ry, 0);
            this.canTake = true;
        },
        // UI层的下棋方法
        take(i, j, role) {
            if (this.canTake || role == 0) {
                this.$set(this.boardData[i], j, role);
                if (role == 1) {
                    this.canTake = false;
                    setTimeout(this.machineTake, 300)
                }
                this.callbackOnChange();
            }
        }
    }
}
</script>

<style scoped>
    .cell {
        width: 30px;
        height: 30px;
        display: table-cell;
    }
    .cross {
        text-align: center;
        vertical-align: middle;
        border: 1px solid rgba(0, 0, 0, 0);
    }
    .square {
        border: 1px solid black;
    }
    .piece {
        cursor: pointer;
    }
    .board {
        position: absolute;
    }
    .play {
        left: 0px;
        top: 0px;
    }
    .mesh {
        left: 15px;
        top: 15px;
    }
</style>