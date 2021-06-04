<template>
    <div class="collapsible" v-bind:class="{ collapsed: collapsed }" style="overflow: hidden;" v-bind:style="{ height: renderedHeight, width: renderedWidth, display: display }" ref="target">
        <slot></slot>
    </div>
</template>

<script>
export default {
    name: 'collapsible',

    components: {

    },

    created: function() {
        this.collapsed = this.state === "collapsed";
    },

    mounted: function() {
        this.$root.$on("collapse-toggle", this.toggle);
        this.$nextTick(() => {
            this.width = this.$refs.target.clientWidth;
            this.height = this.$refs.target.clientHeight;
            this.ready = true;
        });
    },

    props: {
        direction: { // One of horizontal or vertical
            type: String,
            required: true,
        },
        name: {
            type: String,
            required: true,
        },
        state: { //expanded or collapsed
            type: String,
            required: true,
        },
    },

    computed: {
        renderedWidth: function() {
            return this.ready ? (this.width + this.widthDifference) + "px" : "";
        },
        renderedHeight: function() {
            return this.ready ? (this.height + this.heightDifference) + "px" : "";
        },
    },

    data: function() {
        return {
            display: "block",
            lastTime: 0,
            ready: false,
            width: 0,
            height: 0,
            widthDifference: 0,
            heightDifference: 0,
            collapsed: false,
        }
    },

    methods: {
        toggle: function(target) {
            if(this.name === target) {
                window.requestAnimationFrame(this.step);
                //this.collapsed = !this.collapsed;
                //this.display = this.collapsed ? "none" : "block";
            }
        },
        step: function(timestamp) {
            let delta = this.calculateDelta(timestamp);
            let movement = -1;
            if(this.direction === "horizontal") {
                movement = this.stepHorizontal(delta);
            }
            else if(this.direction === "vertical") {
                movement = this.stepVertical(delta);
            }
            if(movement > 0) {
                window.requestAnimationFrame(this.step);
            }
        },
        calculateDelta: function(timestamp) {
            let delta = timestamp - this.lastTime;
            this.lastTime = timestamp;
            return delta / 1000;
        },
        stepHorizontal: function(delta) {

        },
        stepVertical: function(delta) {
            let movement = 10 * delta * (this.collapsed ? 1 : -1);
            this.heightDifference += movement;
            console.log(this.heightDifference);
            return Math.abs(movement);
        },
    },

    filters: {

    },
};
</script>
