def Numeral(
        value=None,
        prefix='',
        separator=True,
        suffix='',
        **kwargs
):
    text = '{}{}{}'.format(prefix, value, suffix)

    return Text(
        markup=text,
        **kwargs,
    )