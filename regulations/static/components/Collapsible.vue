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
        
    },

    mounted: function() {
        this.$root.$on("collapse-toggle", this.toggle);
        this.$nextTick(() => {
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
        collapsed: {
            type: Boolean,
            required: true,
        },
    },

    computed: {
        renderedWidth: function() {
            return this.ready ? (this.$refs.target.clientWidth + this.widthDifference) + "px" : "";
        },
        renderedHeight: function() {
            return this.ready ? (this.$refs.target.clientHeight + this.heightDifference) + "px" : "";
        },
    },

    data: function() {
        return {
            display: "block",
            start: -1.0,
            ready: false,
            widthDifference: 0,
            heightDifference: 0,
        }
    },

    methods: {
        toggle: function(target) {
            if(this.name === target) {
                
                this.collapsed = !this.collapsed;
                this.display = this.collapsed ? "none" : "block";
            }
        },
        stepLeft: function(delta) {

        },
        stepUp: function(delta) {

        },
    },

    filters: {

    },
};
</script>
