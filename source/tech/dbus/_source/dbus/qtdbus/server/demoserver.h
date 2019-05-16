#ifndef DEMOSERVER_H
#define DEMOSERVER_H

#include "demoifadaptor.h"

class DemoServer:public DemoIfAdaptor
{
    Q_OBJECT
public:
    DemoServer(QObject *parent);
    virtual ~DemoIfAdaptor();

public: // PROPERTIES
public Q_SLOTS: // METHODS
    void SayBye();
    void SayHello(const QString &name, const QVariantMap &customdata);
Q_SIGNALS: // SIGNALS
    void LateEvent(const QString &eventkind);
};

#endif
