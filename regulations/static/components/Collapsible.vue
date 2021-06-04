<template>
    <div ref="target" v-bind:class="{ visible: visible }" v-bind:style="[styles, visible ? { height: height } : { height: 0 }]">
        <slot></slot>
    </div>
</template>

<script>
export default {
    name: 'collapsible',

    created: function() {
        this.visible = this.state === "expanded";
        this.$root.$on("collapse-toggle", this.toggle);
    },

    mounted: function() {
        this.$nextTick(() => {
            this.computeHeight();
        });
    },

    props: {
        name: {
            type: String,
            required: true,
        },
        state: { //expanded or collapsed
            type: String,
            required: true,
        },
        transition: {
            type: String,
            required: false,
            default: "1s",
        },
    },

    data: function() {
        return {
            height: 0,
            visible: true,
            styles: {
                overflow: 'hidden',
                transition: this.transition,
            }
        }
    },

    methods: {
        toggle: function(target) {
            if(this.name === target) {
                this.visible = !this.visible;
            }
        },
        computeHeight: function() {
            let setProps = (visibility, display, height, position) => {
                this.$refs.target.style.visibility = visibility;
                this.$refs.target.style.display = display;
                this.$refs.target.style.height = height;
                this.$refs.target.style.position = position;
            };

            setProps("hidden", "block", "auto", "absolute");
            this.height = window.getComputedStyle(this.$refs.target).height;
            setProps(null, null, 0, null);
        },
    },
};
</script>
