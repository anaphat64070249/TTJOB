from service import AppServer;


app = AppServer();

if __name__=="__main__":
    app.run(
        debug=True,
    );