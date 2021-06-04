import Collapsible from '../components/Collapsible.vue';
import CollapseButton from '../components/CollapseButton.vue';

export default {
  title: 'Site/Collapsible',
  component: Collapsible,
  subcomponents: { CollapseButton },
};

const Template = (args, { argTypes }) => ({
  props: Object.keys(argTypes),
  components: { Collapsible, CollapseButton },
  template: '<div><collapse-button name="default" state="collapsed" /><collapsible v-bind="$props">Hello, world!</collapsible></div>',
});

export const Basic = Template.bind({});
Basic.args = {
    "name": "default",
    "state": "collapsed",
};
