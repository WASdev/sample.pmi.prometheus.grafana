import sys
import os

global  AdminConfig

def getNodeId (prompt):
    nodeList = AdminConfig.list("Node").split("\n")

    if (len(nodeList) == 1):
        node = nodeList[0]
    else:
        print ""
        print "Available Nodes:"

        nodeNameList = []

        for item in nodeList:
            item = item.rstrip()
            name = getName(item) 

            nodeNameList.append(name)
            print "   " + name

        DefaultNode = nodeNameList[0]
        if (prompt == ""):
            prompt = "Select the desired node"

        nodeName = getValidInput(prompt+" ["+DefaultNode+"]:", DefaultNode, nodeNameList )

        index = nodeNameList.index(nodeName)
        node = nodeList[index]

    return node

def getServerId (prompt):
    serverList = AdminConfig.list("Server").split("\n")

    if (len(serverList) == 1):
        server = serverList[0]
    else:
        print ""
        print "Available Servers:"

        serverNameList = []

        for item in serverList:
            item = item.rstrip()
            name = getName(item)

            serverNameList.append(name)
            print "   " + name

        DefaultServer = serverNameList[0]
        if (prompt == ""):
            prompt = "Select the desired server"
        serverName = getValidInput(prompt+" ["+DefaultServer+"]:", DefaultServer, serverNameList )

        index = serverNameList.index(serverName)
        server = serverList[index]

    return server

def getName (objectId):
    endIndex = (objectId.find("(c") - 1)
    stIndex = 0
    if (objectId.find("\"") == 0):
        stIndex = 1
    return objectId[stIndex:endIndex+1]

node = getName(getNodeId(""))
server = getName(getServerId(""))

print "Installing Default application ..."

parms = "-appname DefaultApplication"
parms += " -node " + node + " -server " + server
parms += " -nouseMetaDataFromBinary"
app = AdminApp.install("/opt/IBM/WebSphere/AppServer/installableApps/DefaultApplication.ear", [parms])

AdminConfig.save()

print "Installing Metrics application ..."

metricsParms = "-appname MetricsApp"
metricsParms += " -node " + node + " -server " + server
metricsParms += " -nouseMetaDataFromBinary"
metricsApp = AdminApp.install("/opt/IBM/WebSphere/AppServer/installableApps/metrics.ear", [metricsParms])

AdminTask.setGenericJVMArguments('[-nodeName ' + node + ' -serverName ' + server + ' -genericJvmArguments "-Xnoloa"]')

AdminConfig.save()