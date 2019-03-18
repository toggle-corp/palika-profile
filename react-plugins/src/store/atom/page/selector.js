import { createSelector } from 'reselect';

const emptyObject = {};
const emptyList = [];
const emptyFaramState = {
    faramValues: {},
    faramErrors: {},
    // pristine: true,
};

const generatorAddPageSelector = ({ page }) => page.generatorAdd || emptyObject;

export const generatorSelectorGP = createSelector(
    generatorAddPageSelector,
    page => page.generator || emptyObject,
);

export const exportStatusSelectorGP = createSelector(
    generatorAddPageSelector,
    page => page.exportStatus,
);

export const exportStateSelectorGP = createSelector(
    generatorAddPageSelector,
    page => page.exportState || emptyObject,
);

export const generatorErrorListSelectorGP = createSelector(
    generatorSelectorGP,
    generator => generator.errors || emptyList,
);

export const generatorGeoMetaSelectorGP = createSelector(
    generatorSelectorGP,
    generator => generator.geoMeta || emptyObject,
);

export const generatorProvinceListSelectorGP = createSelector(
    generatorGeoMetaSelectorGP,
    geoMeta => geoMeta.provinces || emptyList,
);

export const generatorDistrictListSelectorGP = createSelector(
    generatorGeoMetaSelectorGP,
    geoMeta => geoMeta.districts || emptyList,
);

export const generatorPalikaCodeListSelectorGP = createSelector(
    generatorGeoMetaSelectorGP,
    geoMeta => geoMeta.palikaCodes || emptyList,
);
