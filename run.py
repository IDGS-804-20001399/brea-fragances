from app import create_app
app = create_app()


@app.template_filter()
def moneyFormat(value):
    return "${:,.2f}".format(value)


if __name__ == '__main__':
    app.run(debug=True)
