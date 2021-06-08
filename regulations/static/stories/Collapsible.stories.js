import VerticalCollapsible from '../components/VerticalCollapsible.vue';
import CollapseButton from '../components/CollapseButton.vue';

export default {
  title: 'Site/Collapsible',
  component: CollapseButton,
  subcomponents: { VerticalCollapsible },
};

const Template = (args, { argTypes }) => ({
  props: Object.keys(argTypes),
  components: { VerticalCollapsible, CollapseButton },
  template: `
    <div>
      <collapse-button v-bind="$props" />
      <vertical-collapsible name="default" state="collapsed">Hello, world!</vertical-collapsible>
      <hr />
    </div>`,
});

export const Basic = Template.bind({});
Basic.args = {
    "name": "default",
    "state": "collapsed",
};
